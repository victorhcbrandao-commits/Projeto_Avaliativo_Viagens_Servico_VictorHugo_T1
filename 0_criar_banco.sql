-- ============================================================
-- PROJETO AVALIATIVO - VIAGENS A SERVIÇO
-- Fase 0 - Criação das tabelas Raw e Silver
-- ============================================================

DROP TABLE IF EXISTS gold_transporte_uso CASCADE;
DROP TABLE IF EXISTS gold_destino_custo_medio CASCADE;
DROP TABLE IF EXISTS gold_orgao_custo_total CASCADE;
DROP TABLE IF EXISTS silver_trecho CASCADE;
DROP TABLE IF EXISTS silver_passagem CASCADE;
DROP TABLE IF EXISTS silver_pagamento CASCADE;
DROP TABLE IF EXISTS silver_viagem CASCADE;
DROP TABLE IF EXISTS raw_trecho CASCADE;
DROP TABLE IF EXISTS raw_passagem CASCADE;
DROP TABLE IF EXISTS raw_pagamento CASCADE;
DROP TABLE IF EXISTS raw_viagem CASCADE;

-- CAMADA RAW: cópia fiel do CSV, todas as colunas como texto e sem constraints.
CREATE TABLE raw_viagem (
    id_viagem VARCHAR(30), num_proposta VARCHAR(30), situacao VARCHAR(100), viagem_urgente VARCHAR(20),
    justificativa_urgencia_viagem TEXT, cod_orgao_superior VARCHAR(30), nome_orgao_superior VARCHAR(255),
    cod_orgao_solicitante VARCHAR(30), nome_orgao_solicitante VARCHAR(255), cpf_viajante VARCHAR(30),
    nome_viajante VARCHAR(255), cargo VARCHAR(255), funcao VARCHAR(80), descricao_funcao VARCHAR(255),
    data_inicio VARCHAR(20), data_fim VARCHAR(20), destinos TEXT, motivo TEXT,
    valor_diarias VARCHAR(30), valor_passagens VARCHAR(30), valor_devolucao VARCHAR(30), valor_outros_gastos VARCHAR(30)
);

CREATE TABLE raw_pagamento (
    id_viagem VARCHAR(30), num_proposta VARCHAR(30), cod_orgao_superior VARCHAR(30), nome_orgao_superior VARCHAR(255),
    cod_orgao_pagador VARCHAR(30), nome_orgao_pagador VARCHAR(255), cod_unidade_gestora_pagadora VARCHAR(30),
    nome_unidade_gestora_pagadora VARCHAR(255), tipo_pagamento VARCHAR(80), valor VARCHAR(30)
);

CREATE TABLE raw_passagem (
    id_viagem VARCHAR(30), num_proposta VARCHAR(30), meio_transporte VARCHAR(80), pais_origem_ida VARCHAR(80),
    uf_origem_ida VARCHAR(80), cidade_origem_ida VARCHAR(120), pais_destino_ida VARCHAR(80), uf_destino_ida VARCHAR(80),
    cidade_destino_ida VARCHAR(120), pais_origem_volta VARCHAR(80), uf_origem_volta VARCHAR(80), cidade_origem_volta VARCHAR(120),
    pais_destino_volta VARCHAR(80), uf_destino_volta VARCHAR(80), cidade_destino_volta VARCHAR(120),
    valor_passagem VARCHAR(30), taxa_servico VARCHAR(30), data_emissao VARCHAR(20), hora_emissao VARCHAR(20)
);

CREATE TABLE raw_trecho (
    id_viagem VARCHAR(30), num_proposta VARCHAR(30), sequencia_trecho VARCHAR(20), origem_data VARCHAR(20),
    origem_pais VARCHAR(80), origem_uf VARCHAR(80), origem_cidade VARCHAR(120), destino_data VARCHAR(20),
    destino_pais VARCHAR(80), destino_uf VARCHAR(80), destino_cidade VARCHAR(120), meio_transporte VARCHAR(80),
    numero_diarias VARCHAR(30), missao VARCHAR(20)
);

-- CAMADA SILVER: dados limpos, tipados, com PK, FK e constraints.
CREATE TABLE silver_viagem (
    id_viagem VARCHAR(30) PRIMARY KEY,
    num_proposta VARCHAR(30), situacao VARCHAR(100), viagem_urgente VARCHAR(20), cod_orgao_superior VARCHAR(30),
    nome_orgao_superior VARCHAR(255) NOT NULL, cod_orgao_solicitante VARCHAR(30), nome_orgao_solicitante VARCHAR(255),
    nome_viajante VARCHAR(255), cargo VARCHAR(255), data_inicio DATE, data_fim DATE, destinos TEXT, motivo TEXT,
    valor_diarias DECIMAL(10,2) CHECK (valor_diarias >= 0), valor_passagens DECIMAL(10,2) CHECK (valor_passagens >= 0),
    valor_devolucao DECIMAL(10,2) CHECK (valor_devolucao >= 0), valor_outros_gastos DECIMAL(10,2) CHECK (valor_outros_gastos >= 0),
    valor_total DECIMAL(12,2) CHECK (valor_total >= 0), duracao_dias INT CHECK (duracao_dias >= 0)
);

CREATE TABLE silver_pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_viagem VARCHAR(30) NOT NULL,
    num_proposta VARCHAR(30), nome_orgao_pagador VARCHAR(255), nome_unidade_gestora_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(80) NOT NULL, valor DECIMAL(10,2) CHECK (valor >= 0),
    CONSTRAINT fk_pagamento_viagem FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
);

CREATE TABLE silver_passagem (
    id_passagem SERIAL PRIMARY KEY,
    id_viagem VARCHAR(30) NOT NULL,
    meio_transporte VARCHAR(80), pais_origem_ida VARCHAR(80), uf_origem_ida VARCHAR(80), cidade_origem_ida VARCHAR(120),
    pais_destino_ida VARCHAR(80), uf_destino_ida VARCHAR(80), cidade_destino_ida VARCHAR(120),
    valor_passagem DECIMAL(10,2) CHECK (valor_passagem >= 0), taxa_servico DECIMAL(10,2) CHECK (taxa_servico >= 0), data_emissao DATE,
    CONSTRAINT fk_passagem_viagem FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
);

CREATE TABLE silver_trecho (
    id_trecho SERIAL PRIMARY KEY,
    id_viagem VARCHAR(30) NOT NULL,
    sequencia_trecho INT NOT NULL,
    origem_data DATE, origem_pais VARCHAR(80), origem_uf VARCHAR(80), origem_cidade VARCHAR(120),
    destino_data DATE, destino_pais VARCHAR(80), destino_uf VARCHAR(80), destino_cidade VARCHAR(120),
    meio_transporte VARCHAR(80), numero_diarias DECIMAL(10,2) CHECK (numero_diarias >= 0),
    CONSTRAINT fk_trecho_viagem FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT uq_trecho_viagem_seq UNIQUE (id_viagem, sequencia_trecho)
);

CREATE INDEX idx_silver_viagem_orgao ON silver_viagem(nome_orgao_superior);
CREATE INDEX idx_silver_pagamento_tipo ON silver_pagamento(tipo_pagamento);
CREATE INDEX idx_silver_trecho_destino ON silver_trecho(destino_uf, destino_cidade);
