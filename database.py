from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Padrão:'root' e sem senha
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "floricultura_db"

# String de conexão
# O formato é: mysql+mysqlconnector://<usuario>:<senha>@<host>/<nome_do_banco>
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Engine
engine = create_engine(DATABASE_URL, echo=False)

# Cria uma classe
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria classe Base
Base = declarative_base()

def create_tables():
    """
    Função para criar todas as tabelas no banco de dados MySQL.
    """
    print(f"Verificando e criando tabelas no banco de dados MySQL '{DB_NAME}'...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas/verificadas com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar as tabelas: {e}")

