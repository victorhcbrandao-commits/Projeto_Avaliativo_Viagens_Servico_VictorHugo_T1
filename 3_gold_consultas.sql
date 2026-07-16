-- ============================================================
-- CAMADA GOLD E PERGUNTAS DE NEGÓCIO
-- ============================================================

-- 1. Os 5 órgãos com maior custo total
SELECT nome_orgao_superior, SUM(valor_total) AS custo_total
FROM silver_viagem
GROUP BY nome_orgao_superior
ORDER BY custo_total DESC
LIMIT 5;

-- 2. Os 3 destinos com maior custo médio por viagem
SELECT t.destino_uf, t.destino_cidade, AVG(v.valor_total) AS custo_medio_viagem, COUNT(DISTINCT v.id_viagem) AS quantidade_viagens
FROM silver_viagem v
JOIN silver_trecho t ON v.id_viagem = t.id_viagem
WHERE t.destino_cidade IS NOT NULL
GROUP BY t.destino_uf, t.destino_cidade
HAVING COUNT(DISTINCT v.id_viagem) >= 3
ORDER BY custo_medio_viagem DESC
LIMIT 3;

-- 3. A viagem de maior duração e seu custo total
SELECT id_viagem, num_proposta, nome_orgao_superior, destinos, duracao_dias, valor_total
FROM silver_viagem
ORDER BY duracao_dias DESC, valor_total DESC
LIMIT 1;

-- 4. Qual o tipo de pagamento com maior valor médio
SELECT tipo_pagamento, AVG(valor) AS valor_medio, COUNT(*) AS quantidade_pagamentos
FROM silver_pagamento
GROUP BY tipo_pagamento
ORDER BY valor_medio DESC
LIMIT 1;

-- 5. Qual o meio de transporte mais usado nos trechos
SELECT meio_transporte, COUNT(*) AS quantidade_trechos
FROM silver_trecho
WHERE meio_transporte IS NOT NULL
GROUP BY meio_transporte
ORDER BY quantidade_trechos DESC
LIMIT 5;

-- 6. Qual UF de destino aparece em mais trechos
SELECT destino_uf, COUNT(*) AS quantidade_trechos
FROM silver_trecho
WHERE destino_uf IS NOT NULL
GROUP BY destino_uf
ORDER BY quantidade_trechos DESC
LIMIT 10;

-- 7. Qual órgão pagou mais no total
SELECT nome_orgao_pagador, SUM(valor) AS total_pago
FROM silver_pagamento
WHERE nome_orgao_pagador IS NOT NULL
GROUP BY nome_orgao_pagador
ORDER BY total_pago DESC
LIMIT 5;

-- Tabelas Gold materializadas
DROP TABLE IF EXISTS gold_orgao_custo_total;
CREATE TABLE gold_orgao_custo_total AS
SELECT nome_orgao_superior, SUM(valor_total) AS custo_total
FROM silver_viagem
GROUP BY nome_orgao_superior
ORDER BY custo_total DESC;

DROP TABLE IF EXISTS gold_destino_custo_medio;
CREATE TABLE gold_destino_custo_medio AS
SELECT t.destino_uf, t.destino_cidade, AVG(v.valor_total) AS custo_medio_viagem, COUNT(DISTINCT v.id_viagem) AS quantidade_viagens
FROM silver_viagem v
JOIN silver_trecho t ON v.id_viagem = t.id_viagem
WHERE t.destino_cidade IS NOT NULL
GROUP BY t.destino_uf, t.destino_cidade
ORDER BY custo_medio_viagem DESC;

DROP TABLE IF EXISTS gold_transporte_uso;
CREATE TABLE gold_transporte_uso AS
SELECT meio_transporte, COUNT(*) AS quantidade_trechos
FROM silver_trecho
WHERE meio_transporte IS NOT NULL
GROUP BY meio_transporte
ORDER BY quantidade_trechos DESC;
