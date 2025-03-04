import db
from sqlalchemy import Column, VARCHAR, CHAR, Integer

# ORM para Cliente

class ClienteDB(db.Base):
    __tablename__ = 'tb_cliente'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    cpf = Column(CHAR(11), unique=True, nullable=False, index=True)
    telefone = Column(CHAR(11), nullable=False)

    def __init__(self, id_cliente, nome, cpf, telefone):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone