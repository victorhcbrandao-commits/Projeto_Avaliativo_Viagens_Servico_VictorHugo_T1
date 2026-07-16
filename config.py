"""Configurações centrais do projeto. Credenciais ficam no arquivo .env."""
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
LOG_DIR = BASE_DIR / "logs"
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "viagens_servico")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DRIVE_FILE_ID = os.getenv("DRIVE_FILE_ID", "").strip()
ZIP_PATH = BASE_DIR / os.getenv("ZIP_PATH", "data/raw/viagens_2025_6meses.zip")

CSV_CONFIG = {
    "viagem": {"arquivo":"2025_Viagem.csv","tabela_raw":"raw_viagem","colunas":{
        "Identificador do processo de viagem":"id_viagem","Número da Proposta (PCDP)":"num_proposta","Situação":"situacao","Viagem Urgente":"viagem_urgente","Justificativa Urgência Viagem":"justificativa_urgencia_viagem","Código do órgão superior":"cod_orgao_superior","Nome do órgão superior":"nome_orgao_superior","Código órgão solicitante":"cod_orgao_solicitante","Nome órgão solicitante":"nome_orgao_solicitante","CPF viajante":"cpf_viajante","Nome":"nome_viajante","Cargo":"cargo","Função":"funcao","Descrição Função":"descricao_funcao","Período - Data de início":"data_inicio","Período - Data de fim":"data_fim","Destinos":"destinos","Motivo":"motivo","Valor diárias":"valor_diarias","Valor passagens":"valor_passagens","Valor devolução":"valor_devolucao","Valor outros gastos":"valor_outros_gastos"}},
    "pagamento": {"arquivo":"2025_Pagamento.csv","tabela_raw":"raw_pagamento","colunas":{
        "Identificador do processo de viagem":"id_viagem","Número da Proposta (PCDP)":"num_proposta","Código do órgão superior":"cod_orgao_superior","Nome do órgão superior":"nome_orgao_superior","Codigo do órgão pagador":"cod_orgao_pagador","Nome do órgao pagador":"nome_orgao_pagador","Código da unidade gestora pagadora":"cod_unidade_gestora_pagadora","Nome da unidade gestora pagadora":"nome_unidade_gestora_pagadora","Tipo de pagamento":"tipo_pagamento","Valor":"valor"}},
    "passagem": {"arquivo":"2025_Passagem.csv","tabela_raw":"raw_passagem","colunas":{
        "Identificador do processo de viagem":"id_viagem","Número da Proposta (PCDP)":"num_proposta","Meio de transporte":"meio_transporte","País - Origem ida":"pais_origem_ida","UF - Origem ida":"uf_origem_ida","Cidade - Origem ida":"cidade_origem_ida","País - Destino ida":"pais_destino_ida","UF - Destino ida":"uf_destino_ida","Cidade - Destino ida":"cidade_destino_ida","País - Origem volta":"pais_origem_volta","UF - Origem volta":"uf_origem_volta","Cidade - Origem volta":"cidade_origem_volta","Pais - Destino volta":"pais_destino_volta","UF - Destino volta":"uf_destino_volta","Cidade - Destino volta":"cidade_destino_volta","Valor da passagem":"valor_passagem","Taxa de serviço":"taxa_servico","Data da emissão/compra":"data_emissao","Hora da emissão/compra":"hora_emissao"}},
    "trecho": {"arquivo":"2025_Trecho.csv","tabela_raw":"raw_trecho","colunas":{
        "Identificador do processo de viagem ":"id_viagem","Número da Proposta (PCDP)":"num_proposta","Sequência Trecho":"sequencia_trecho","Origem - Data":"origem_data","Origem - País":"origem_pais","Origem - UF":"origem_uf","Origem - Cidade":"origem_cidade","Destino - Data":"destino_data","Destino - País":"destino_pais","Destino - UF":"destino_uf","Destino - Cidade":"destino_cidade","Meio de transporte":"meio_transporte","Número Diárias":"numero_diarias","Missao?":"missao"}},
}
