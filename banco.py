"""Funções utilitárias de conexão e execução SQL no PostgreSQL."""
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def validar_configuracao_banco() -> None:
    if not DB_PASSWORD:
        raise ValueError("Senha do PostgreSQL não informada. Crie o arquivo .env na raiz do projeto e preencha DB_PASSWORD. Use .env.example como modelo.")

def criar_engine() -> Engine:
    validar_configuracao_banco()
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, pool_pre_ping=True)

def testar_conexao() -> None:
    try:
        engine = criar_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Conexão com PostgreSQL realizada com sucesso.")
    except OperationalError as erro:
        raise ConnectionError("Não foi possível conectar ao PostgreSQL. Confira DB_HOST, DB_PORT, DB_NAME, DB_USER e DB_PASSWORD no .env.") from erro

def executar_sql_arquivo(caminho_sql: str) -> None:
    engine = criar_engine()
    with open(caminho_sql, "r", encoding="utf-8") as arquivo:
        sql = arquivo.read()
    with engine.begin() as conn:
        conn.execute(text(sql))
