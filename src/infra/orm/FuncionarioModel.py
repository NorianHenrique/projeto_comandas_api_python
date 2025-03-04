from sqlalchemy import Column, VARCHAR, CHAR, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FuncionarioDB(Base):
    __tablename__ = 'tb_funcionario'

    id_funcionario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    matricula = Column(CHAR(10), nullable=False)
    cpf = Column(CHAR(11), unique=True, nullable=False, index=True)
    telefone = Column(CHAR(11), nullable=False)
    grupo = Column(Integer, nullable=False)
    senha = Column(VARCHAR(200), nullable=False)

    # Nenhum método __init__ é necessário aqui.
