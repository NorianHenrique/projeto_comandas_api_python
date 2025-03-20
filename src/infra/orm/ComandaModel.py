import db
from sqlalchemy import Column, VARCHAR, Integer, DateTime, DECIMAL, ForeignKey
from infra.orm.ProdutoModel import ProdutoDB
from infra.orm.FuncionarioModel import FuncionarioDB
from infra.orm.ClienteModel import ClienteDB

# ORM
class ComandaDB(db.Base):
    __tablename__ = 'tb_comanda'
    id_comanda = Column(Integer, primary_key=True, autoincrement=True, index=True)
    comanda = Column(VARCHAR(100), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)
    funcionario_id = Column(Integer, ForeignKey('tb_funcionario.id_funcionario'), nullable=False)
    cliente_id = Column(Integer, ForeignKey('tb_cliente.id_cliente'), nullable=True, default=None)

    def __init__(self, id_comanda, comanda, data_hora, status, funcionario_id, cliente_id):
        self.id_comanda = id_comanda
        self.comanda = comanda
        self.data_hora = data_hora
        self.status = status
        self.funcionario_id = funcionario_id
        self.cliente_id = cliente_id

class ComandaProdutoDB(db.Base):
    __tablename__ = 'tb_comanda_produto'
    id_comanda_produto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    comanda_id = Column(Integer, ForeignKey('tb_comanda.id_comanda'), nullable=False)
    produto_id = Column(Integer, ForeignKey('tb_produto.id_produto'), nullable=False)
    funcionario_id = Column(Integer, ForeignKey('tb_funcionario.id_funcionario'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(DECIMAL, nullable=False)

    def __init__(self, id_comanda_produto, comanda_id, produto_id, funcionario_id, quantidade, valor_unitario):
        self.id_comanda_produto = id_comanda_produto
        self.comanda_id = comanda_id
        self.produto_id = produto_id
        self.funcionario_id = funcionario_id
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario