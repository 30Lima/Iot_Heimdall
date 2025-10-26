import os
import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# --- 1. Carregar Variáveis de Ambiente ---
# Lê o ficheiro .env para proteger as suas credenciais
load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_SERVICE = os.environ.get("DB_SERVICE_NAME")

# Validação (segurança)
if not all([DB_USER, DB_PASS, DB_HOST, DB_SERVICE]):
    raise ValueError("Erro: As variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_SERVICE não estão configuradas no ficheiro .env")

# --- 2. Construir a String de Conexão (DSN) ---
# Formato padrão para SQLAlchemy + Oracle + cx_Oracle
# cx_Oracle espera o formato DSN (Data Source Name)
dsn = f"{DB_HOST}:1521/{DB_SERVICE}"
DATABASE_URI = f"oracle+cx_oracle://{DB_USER}:{DB_PASS}@{dsn}"

# --- 3. Configurar o SQLAlchemy ---
# O 'engine' é o "motor" que gere a ligação
# pool_pre_ping=True verifica se a ligação está viva antes de a usar (bom para Oracle)
engine = create_engine(DATABASE_URI, pool_pre_ping=True)

# A 'session' é o "canal" que usamos para falar com a base de dados
# Usamos scoped_session para garantir que cada thread (Flask, MQTT) tenha a sua própria sessão
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# 'Base' é a classe-mãe que os nossos modelos (tabelas) vão herdar
Base = declarative_base()
Base.query = db_session.query_property()

# --- 4. Definir o Modelo (A Tabela) ---
# Esta classe é o "mapa" da sua tabela `telemetria` no Oracle.
class Telemetria(Base):
    __tablename__ = "telemetria"  # Nome da tabela no Oracle
    
    # Colunas
    id = Column(Integer, primary_key=True, autoincrement=True)
    moto_id = Column(String(50), nullable=False)
    zona = Column(String(50))
    vaga = Column(String(50))
    status = Column(String(50)) # ex: "entrada", "saida"
    correct = Column(Boolean) # ex: True ou False
    timestamp = Column(DateTime, default=datetime.datetime.now) # Data e hora do evento

    def to_dict(self):
        """Função útil para transformar os dados em JSON para a API."""
        return {
            "id": self.id,
            "moto_id": self.moto_id,
            "zona": self.zona,
            "vaga": self.vaga,
            "status": self.status,
            "correct": self.correct,
            # Formata a data para um padrão que o JavaScript entende (ISO 8601)
            "timestamp": self.timestamp.isoformat() 
        }

# --- 5. Função para Criar as Tabelas ---
def init_db():
    """
    Função para criar as tabelas no Oracle.
    Vamos executar isto uma vez a partir do nosso ficheiro run.py.
    """
    print("A criar tabelas na base de dados (se não existirem)...")
    # O Base.metadata.create_all(engine) lê todos os modelos que herdam de 'Base'
    # e cria as tabelas correspondentes no Oracle.
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso (ou já existentes).")