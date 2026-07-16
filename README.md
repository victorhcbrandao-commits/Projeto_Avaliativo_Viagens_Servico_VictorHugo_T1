# Projeto Avaliativo - Pipeline de Viagens a Serviço

**Curso:** Análise de Dados com Python [T1]  
**Módulo:** 1 - Semana 13  
**Aluno:** Victor Hugo  
**Arquitetura:** Medallion Architecture - Raw, Silver e Gold  

---

## 1. Contextualização

O Portal da Transparência disponibiliza dados públicos de viagens a serviço do Governo Federal. Esses dados chegam em CSVs brutos, com formatos variados, valores monetários em padrão brasileiro, datas em texto e informações espalhadas em múltiplos arquivos.

Este projeto transforma esses dados brutos em informação confiável, estruturada e pronta para análise, utilizando Python, SQL e PostgreSQL.

---

## 2. Objetivo

Construir um pipeline de dados completo que:

- baixa ou recebe o ZIP de origem;
- preserva os dados brutos na camada Raw;
- limpa e tipa os dados na camada Silver;
- cria uma camada Gold com consultas, agregações e gráficos;
- responde às perguntas de negócio do projeto avaliativo.

---

## 3. Tecnologias utilizadas

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Psycopg2
- Jupyter Notebook
- Matplotlib
- gdown / Google Drive
- Git e GitHub
- `.env` para credenciais

---

## 4. Estrutura do projeto

```text
Projeto_Avaliativo_Viagens_Servico_VictorHugo_T1/
├── config.py
├── banco.py
├── 0_criar_banco.sql
├── 1_extrair.py
├── 2_transformar.py
├── 3_analise.ipynb
├── 3_gold_consultas.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── COMANDOS_GITHUB.md
├── data/
│   ├── raw/
│   │   └── README.md
│   └── sample/
│       ├── amostra_2025_Viagem.csv
│       ├── amostra_2025_Pagamento.csv
│       ├── amostra_2025_Passagem.csv
│       └── amostra_2025_Trecho.csv
└── docs/
    └── DICIONARIO_DADOS.md
```

---

## 5. Pipeline

### 5.1 Camada Raw

A camada Raw preserva o conteúdo original dos CSVs. Todas as colunas são criadas como texto, sem constraints, garantindo rastreabilidade e auditoria.

Tabelas:

- `raw_viagem`
- `raw_pagamento`
- `raw_passagem`
- `raw_trecho`

### 5.2 Camada Silver

A camada Silver contém dados tratados, tipados e organizados em tabelas relacionais.

Foram aplicados:

- conversão de texto para `DATE`;
- conversão de texto para `DECIMAL`;
- limpeza de textos;
- remoção de duplicidades;
- cálculo de `valor_total`;
- cálculo de `duracao_dias`;
- chaves primárias;
- chaves estrangeiras;
- constraints `NOT NULL`, `CHECK` e `UNIQUE`.

Tabelas:

- `silver_viagem`
- `silver_pagamento`
- `silver_passagem`
- `silver_trecho`

### 5.3 Camada Gold

A camada Gold responde às perguntas de negócio usando SQL com `JOIN`, `GROUP BY`, agregações e gráficos.

---

## 6. Como executar

### 6.1 Criar ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

### 6.2 Criar o arquivo `.env`

O arquivo `.env` não vem criado no repositório porque contém credenciais do banco de dados.

Crie manualmente um arquivo chamado exatamente:

```text
.env
```

na raiz do projeto.

Depois, copie o conteúdo de `.env.example` para dentro dele e preencha sua senha do PostgreSQL:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=viagens_servico
DB_USER=postgres
DB_PASSWORD=SUA_SENHA_DO_POSTGRES

DRIVE_FILE_ID=
ZIP_PATH=data/raw/viagens_2025_6meses.zip
```

Se quiser usar download automático pelo Google Drive, preencha também o `DRIVE_FILE_ID`.

Se preferir execução local, deixe `DRIVE_FILE_ID` vazio e coloque o arquivo:

```text
viagens_2025_6meses.zip
```

na pasta:

```text
data/raw/
```

---

### 6.3 Criar banco PostgreSQL

No PostgreSQL ou pgAdmin, crie o banco:

```sql
CREATE DATABASE viagens_servico;
```

---

### 6.4 Executar scripts na ordem

```bash
python 1_extrair.py
python 2_transformar.py
jupyter notebook 3_analise.ipynb
```

O script `1_extrair.py` executa automaticamente o arquivo `0_criar_banco.sql`.

Após abrir o Jupyter Notebook:

- selecione o kernel **Python 3 (ipykernel)**;
- clique em **Run → Run All Cells** (ou **Run All**);
- aguarde a execução completa.

O notebook irá:

- responder todas as perguntas de negócio;
- gerar os gráficos;
- criar as tabelas da camada Gold.

---

## 7. Perguntas de negócio respondidas

1. Os 5 órgãos com maior custo total;
2. Os 3 destinos com maior custo médio por viagem;
3. A viagem de maior duração e seu custo total;
4. Qual o tipo de pagamento com maior valor médio;
5. Qual o meio de transporte mais usado nos trechos;
6. Qual UF de destino aparece em mais trechos;
7. Qual órgão pagou mais no total.

---

## 8. Melhorias possíveis

- Criar dashboard em Power BI, Tableau ou Streamlit;
- Criar agendamento automático do pipeline;
- Adicionar testes automatizados de qualidade;
- Salvar logs de execução;
- Criar mais tabelas Gold;
- Publicar visualizações em uma página web.

---

## 9. Conclusão

O projeto demonstra a importância de um pipeline ETL bem estruturado para transformar dados públicos brutos em informações confiáveis. A arquitetura Raw, Silver e Gold garante rastreabilidade, qualidade, organização e facilidade de análise.

A camada Silver melhora a integridade dos dados por meio de tipos corretos, chaves e constraints. A camada Gold torna a informação acessível por meio de consultas de negócio e gráficos.

---

## 10. Versionamento

O projeto deve ser enviado ao GitHub em repositório público, com commits descritivos e separados por funcionalidade.

Sugestão de commits:

```bash
git add 0_criar_banco.sql config.py banco.py requirements.txt .env.example .gitignore
git commit -m "Cria estrutura inicial e modelagem do banco"

git add 1_extrair.py
git commit -m "Implementa extracao e carga da camada raw"

git add 2_transformar.py
git commit -m "Implementa transformacao e carga da camada silver"

git add 3_analise.ipynb 3_gold_consultas.sql
git commit -m "Implementa camada gold e perguntas de negocio"

git add README.md COMANDOS_GITHUB.md docs/ data/sample/ data/raw/README.md
git commit -m "Finaliza documentacao e organizacao do projeto"
```
