# Dicionário de Dados - Camada Silver

## `silver_viagem`

| Coluna | Tipo | Restrições / Tratamento |
|---|---|---|
| id_viagem | VARCHAR(30) | PRIMARY KEY, NOT NULL |
| num_proposta | VARCHAR(30) | Número da proposta |
| situacao | VARCHAR(100) | Texto tratado |
| viagem_urgente | VARCHAR(20) | Texto tratado |
| cod_orgao_superior | VARCHAR(30) | Código do órgão superior |
| nome_orgao_superior | VARCHAR(255) | NOT NULL |
| cod_orgao_solicitante | VARCHAR(30) | Código do órgão solicitante |
| nome_orgao_solicitante | VARCHAR(255) | Texto tratado |
| nome_viajante | VARCHAR(255) | Texto tratado |
| cargo | VARCHAR(255) | Texto tratado |
| data_inicio | DATE | Convertido de DD/MM/AAAA |
| data_fim | DATE | Convertido de DD/MM/AAAA |
| destinos | TEXT | Texto tratado |
| motivo | TEXT | Texto tratado |
| valor_diarias | DECIMAL(10,2) | CHECK >= 0 |
| valor_passagens | DECIMAL(10,2) | CHECK >= 0 |
| valor_devolucao | DECIMAL(10,2) | CHECK >= 0 |
| valor_outros_gastos | DECIMAL(10,2) | CHECK >= 0 |
| valor_total | DECIMAL(12,2) | Calculado, CHECK >= 0 |
| duracao_dias | INT | Calculado, CHECK >= 0 |

## `silver_pagamento`

| Coluna | Tipo | Restrições / Tratamento |
|---|---|---|
| id_pagamento | SERIAL | PRIMARY KEY |
| id_viagem | VARCHAR(30) | FOREIGN KEY, NOT NULL |
| num_proposta | VARCHAR(30) | Número da proposta |
| nome_orgao_pagador | VARCHAR(255) | Texto tratado |
| nome_unidade_gestora_pagadora | VARCHAR(255) | Texto tratado |
| tipo_pagamento | VARCHAR(80) | NOT NULL |
| valor | DECIMAL(10,2) | CHECK >= 0 |

## `silver_passagem`

| Coluna | Tipo | Restrições / Tratamento |
|---|---|---|
| id_passagem | SERIAL | PRIMARY KEY |
| id_viagem | VARCHAR(30) | FOREIGN KEY, NOT NULL |
| meio_transporte | VARCHAR(80) | Texto tratado |
| valor_passagem | DECIMAL(10,2) | CHECK >= 0 |
| taxa_servico | DECIMAL(10,2) | CHECK >= 0 |
| data_emissao | DATE | Convertido de DD/MM/AAAA |

## `silver_trecho`

| Coluna | Tipo | Restrições / Tratamento |
|---|---|---|
| id_trecho | SERIAL | PRIMARY KEY |
| id_viagem | VARCHAR(30) | FOREIGN KEY, NOT NULL |
| sequencia_trecho | INT | NOT NULL |
| origem_data | DATE | Convertido de DD/MM/AAAA |
| destino_data | DATE | Convertido de DD/MM/AAAA |
| meio_transporte | VARCHAR(80) | Texto tratado |
| numero_diarias | DECIMAL(10,2) | CHECK >= 0 |
| uq_trecho_viagem_seq | UNIQUE | id_viagem + sequencia_trecho |
