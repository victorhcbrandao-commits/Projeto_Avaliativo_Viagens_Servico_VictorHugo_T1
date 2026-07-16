"""Fase 2 - Transformação Raw -> Silver."""
import re
import pandas as pd
from sqlalchemy import text
from banco import criar_engine, testar_conexao


def limpar_texto(valor):
    if pd.isna(valor):
        return None
    valor = str(valor).strip()
    if valor == "" or valor.lower() in {"nan", "sem informação", "sem informacao"}:
        return None
    return re.sub(r"\s+", " ", valor)


def decimal_br(valor):
    if pd.isna(valor):
        return 0.0
    valor = str(valor).strip()
    if valor == "" or valor.lower() in {"nan", "sem informação", "sem informacao"}:
        return 0.0
    valor = valor.replace(".", "").replace(",", ".")
    try:
        return max(float(valor), 0.0)
    except ValueError:
        return 0.0


def data_br(serie):
    return pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")


def truncar_silver(engine):
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE silver_trecho, silver_passagem, silver_pagamento, silver_viagem RESTART IDENTITY CASCADE;"))


def transformar_viagem(engine):
    print("Transformando raw_viagem -> silver_viagem...")
    df = pd.read_sql("SELECT * FROM raw_viagem", engine)
    df["id_viagem"] = df["id_viagem"].astype(str).str.strip()
    df = df[df["id_viagem"] != ""].drop_duplicates(subset=["id_viagem"])
    for coluna in ["num_proposta", "situacao", "viagem_urgente", "cod_orgao_superior", "nome_orgao_superior", "cod_orgao_solicitante", "nome_orgao_solicitante", "nome_viajante", "cargo", "destinos", "motivo"]:
        df[coluna] = df[coluna].apply(limpar_texto)
    df["nome_orgao_superior"] = df["nome_orgao_superior"].fillna("Órgão não informado")
    df["data_inicio"] = data_br(df["data_inicio"])
    df["data_fim"] = data_br(df["data_fim"])
    for coluna in ["valor_diarias", "valor_passagens", "valor_devolucao", "valor_outros_gastos"]:
        df[coluna] = df[coluna].apply(decimal_br)
    df["valor_total"] = (df["valor_diarias"] + df["valor_passagens"] + df["valor_outros_gastos"] - df["valor_devolucao"]).clip(lower=0)
    df["duracao_dias"] = (df["data_fim"] - df["data_inicio"]).dt.days.fillna(0).clip(lower=0).astype(int)
    silver = df[["id_viagem", "num_proposta", "situacao", "viagem_urgente", "cod_orgao_superior", "nome_orgao_superior", "cod_orgao_solicitante", "nome_orgao_solicitante", "nome_viajante", "cargo", "data_inicio", "data_fim", "destinos", "motivo", "valor_diarias", "valor_passagens", "valor_devolucao", "valor_outros_gastos", "valor_total", "duracao_dias"]]
    silver.to_sql("silver_viagem", engine, if_exists="append", index=False, method="multi", chunksize=5000)
    print(f"silver_viagem: {len(silver):,} registros")


def transformar_pagamento(engine):
    print("Transformando raw_pagamento -> silver_pagamento...")
    df = pd.read_sql("SELECT p.* FROM raw_pagamento p INNER JOIN silver_viagem v ON p.id_viagem = v.id_viagem", engine)
    df["tipo_pagamento"] = df["tipo_pagamento"].apply(limpar_texto).fillna("Não informado")
    df["nome_orgao_pagador"] = df["nome_orgao_pagador"].apply(limpar_texto)
    df["nome_unidade_gestora_pagadora"] = df["nome_unidade_gestora_pagadora"].apply(limpar_texto)
    df["valor"] = df["valor"].apply(decimal_br)
    silver = df[["id_viagem", "num_proposta", "nome_orgao_pagador", "nome_unidade_gestora_pagadora", "tipo_pagamento", "valor"]].drop_duplicates()
    silver.to_sql("silver_pagamento", engine, if_exists="append", index=False, method="multi", chunksize=5000)
    print(f"silver_pagamento: {len(silver):,} registros")


def transformar_passagem(engine):
    print("Transformando raw_passagem -> silver_passagem...")
    df = pd.read_sql("SELECT p.* FROM raw_passagem p INNER JOIN silver_viagem v ON p.id_viagem = v.id_viagem", engine)
    for coluna in ["meio_transporte", "pais_origem_ida", "uf_origem_ida", "cidade_origem_ida", "pais_destino_ida", "uf_destino_ida", "cidade_destino_ida"]:
        df[coluna] = df[coluna].apply(limpar_texto)
    df["valor_passagem"] = df["valor_passagem"].apply(decimal_br)
    df["taxa_servico"] = df["taxa_servico"].apply(decimal_br)
    df["data_emissao"] = data_br(df["data_emissao"])
    silver = df[["id_viagem", "meio_transporte", "pais_origem_ida", "uf_origem_ida", "cidade_origem_ida", "pais_destino_ida", "uf_destino_ida", "cidade_destino_ida", "valor_passagem", "taxa_servico", "data_emissao"]].drop_duplicates()
    silver.to_sql("silver_passagem", engine, if_exists="append", index=False, method="multi", chunksize=5000)
    print(f"silver_passagem: {len(silver):,} registros")


def transformar_trecho(engine):
    print("Transformando raw_trecho -> silver_trecho...")
    df = pd.read_sql("SELECT t.* FROM raw_trecho t INNER JOIN silver_viagem v ON t.id_viagem = v.id_viagem", engine)
    df["sequencia_trecho"] = pd.to_numeric(df["sequencia_trecho"], errors="coerce").fillna(0).astype(int)
    df = df[df["sequencia_trecho"] > 0]
    for coluna in ["origem_pais", "origem_uf", "origem_cidade", "destino_pais", "destino_uf", "destino_cidade", "meio_transporte"]:
        df[coluna] = df[coluna].apply(limpar_texto)
    df["origem_data"] = data_br(df["origem_data"])
    df["destino_data"] = data_br(df["destino_data"])
    df["numero_diarias"] = df["numero_diarias"].apply(decimal_br)
    silver = df[["id_viagem", "sequencia_trecho", "origem_data", "origem_pais", "origem_uf", "origem_cidade", "destino_data", "destino_pais", "destino_uf", "destino_cidade", "meio_transporte", "numero_diarias"]].drop_duplicates(subset=["id_viagem", "sequencia_trecho"])
    silver.to_sql("silver_trecho", engine, if_exists="append", index=False, method="multi", chunksize=5000)
    print(f"silver_trecho: {len(silver):,} registros")


def main():
    print("=" * 70)
    print("FASE 2 - TRANSFORMAÇÃO E CAMADA SILVER")
    print("=" * 70)
    testar_conexao()
    engine = criar_engine()
    truncar_silver(engine)
    transformar_viagem(engine)
    transformar_pagamento(engine)
    transformar_passagem(engine)
    transformar_trecho(engine)
    print("Camada Silver criada com sucesso.")


if __name__ == "__main__":
    main()
