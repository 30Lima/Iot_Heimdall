import os
import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_SERVICE = os.environ.get("DB_SERVICE_NAME")

if not all([DB_USER, DB_PASS, DB_HOST, DB_SERVICE]):
    raise ValueError("Erro: As variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_SERVICE não estão configuradas no ficheiro .env")

dsn = f"{DB_HOST}:1521/{DB_SERVICE}"
DATABASE_URI = f"oracle+oracledb://{DB_USER}:{DB_PASS}@{dsn}"

engine = create_engine(DATABASE_URI, pool_pre_ping=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Telemetria(Base):
    __tablename__ = "telemetria" 
    
    id = Column(Integer, Sequence('telemetria_id_seq'), primary_key=True)
    moto_id = Column(String(50), nullable=False)
    zona = Column(String(50))
    vaga = Column(String(50))
    status = Column(String(50)) 
    correct = Column(Boolean) 
    timestamp = Column(DateTime, default=datetime.datetime.now) 

    def to_dict(self):
        """Função útil para transformar os dados em JSON para a API."""
        return {
            "id": self.id,
            "moto_id": self.moto_id,
            "zona": self.zona,
            "vaga": self.vaga,
            "status": self.status,
            "correct": self.correct, 
            "timestamp": self.timestamp.isoformat() 
        }

def init_db():
    """
    Função para criar as tabelas no Oracle.
    Vamos executar isto uma vez a partir do nosso ficheiro run.py.
    """
    print("A criar tabelas na base de dados (se não existirem)...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso (ou já existentes).")