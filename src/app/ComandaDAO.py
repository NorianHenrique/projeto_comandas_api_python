from fastapi import APIRouter
from domain.entities.Comanda import Comanda, ComandaProdutos
# import da persistência
import db
from infra.orm.ComandaModel import ComandaDB, ComandaProdutoDB
from infra.orm.ProdutoModel import ProdutoDB
from infra.orm.FuncionarioModel import FuncionarioDB
from infra.orm.ClienteModel import ClienteDB

# import da segurança
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

#router = APIRouter()
# dependências de forma global
router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Lista comanda conforme o id informado
@router.get("/comanda/{id_comanda}", tags=["Comanda"])
async def get_comanda(id_comanda: int):
    try:
        session = db.Session()

        # busca filtrando pelo status
        aux_dados = session.query(ComandaDB, FuncionarioDB, ClienteDB)\
            .select_from(ComandaDB)\
            .join(FuncionarioDB, FuncionarioDB.id_funcionario == ComandaDB.funcionario_id, isouter=False)\
            .join(ClienteDB, ClienteDB.id_cliente == ComandaDB.cliente_id, isouter=True)\
            .filter(ComandaDB.id_comanda == id_comanda)\
            .order_by(ComandaDB.id_comanda)\
            .all()
        
    # monta o json com o retorno das três tabelas
        dados = []
        for row in aux_dados:
            dados.append({'comanda': row[0], 'funcionario': row[1], 'cliente': row[2]})

        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()


# Lista comandas conforme status informado {0 - aberta, 1 - fechada, 2 - cancelada}
@router.get("/comanda/status/{status}", tags=["Comanda"])
async def get_comanda(status: int):
    try:
        session = db.Session()

        # busca filtrando pelo status
        aux_dados = session.query(ComandaDB, FuncionarioDB, ClienteDB)\
            .select_from(ComandaDB)\
            .join(FuncionarioDB, FuncionarioDB.id_funcionario == ComandaDB.funcionario_id, isouter=False)\
            .join(ClienteDB, ClienteDB.id_cliente == ComandaDB.cliente_id, isouter=True)\
            .filter(ComandaDB.status == status)\
            .order_by(ComandaDB.id_comanda)\
            .all()
        
        print(aux_dados)
        
        # monta o json com o retorno das três tabelas
        dados = []
        for row in aux_dados:
            dados.append({'comanda': row[0], 'funcionario': row[1], 'cliente': row[2]})

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Abre Nova Comanda
@router.post("/comanda", tags=["Comanda"])
async def post_comanda(corpo: Comanda):
    try:
        session = db.Session()

        # antes de abrir a comanda validar se ela já não esta aberta, status == 0
        dados = session.query(ComandaDB).filter(ComandaDB.comanda == corpo.comanda).filter(ComandaDB.status == 0).all()
        if len(dados) > 0:
            # comanda já aberta, retorna o json com seus dados
            return dados, 300
        else:
            # insere a nova comanda
            dados = ComandaDB(None, corpo.comanda, corpo.data_hora, corpo.status, corpo.funcionario_id, corpo.cliente_id)
            session.add(dados)

            # session.flush()

            session.commit()

            return {"id": dados.id_comanda}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Edita Comanda
@router.put("/comanda", tags=["Comanda"])
async def put_comanda(corpo: Comanda):
    try:
        session = db.Session()
        
        # busca os dados atuais da comanda
        dados = session.query(ComandaDB).filter(ComandaDB.id_comanda == corpo.id_comanda).one()

        # atualiza os dados
        #dados.id_comanda == corpo.id_comanda
        dados.comanda = corpo.comanda
        dados.data_hora = corpo.data_hora
        dados.status = corpo.status
        dados.funcionario_id = corpo.funcionario_id
        dados.cliente_id = corpo.cliente_id

        session.add(dados)
        session.commit()
        return {"id": dados.id_comanda}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()


# Adiciona item na Comanda
@router.post("/comanda/item", tags=["Comanda"])
async def post_comanda_item(corpo: ComandaProdutos):
    try:
        session = db.Session()
        # insere um novo item na comanda
        dados = ComandaProdutoDB(None, corpo.comanda_id, corpo.produto_id, corpo.funcionario_id, corpo.quantidade, corpo.valor_unitario)
        session.add(dados)
        #Session.flush()
        session.commit()

        return {"id": dados.id_comanda_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()


# Lista todos os itens da comanda informada
@router.get("/comanda/{comanda_id}/item", tags=["Comanda"])
async def get_comanda_item(comanda_id: int):
    try:
        session = db.Session()
        # busca todos os itens da comanda informada

        aux_dados = session.query(ComandaProdutoDB, FuncionarioDB, ProdutoDB)\
        .select_from(ComandaProdutoDB)\
        .join(FuncionarioDB, FuncionarioDB.id_funcionario == ComandaProdutoDB.funcionario_id, isouter=False)\
        .join(ProdutoDB, ProdutoDB.id_produto == ComandaProdutoDB.produto_id, isouter=False)\
        .filter(ComandaProdutoDB.comanda_id == comanda_id)\
        .order_by(ComandaProdutoDB.quantidade)\
        .all()

        #monta o json com o retorno das três tabelas
        dados = []
        for row in aux_dados:
            dados.append(
            {'comanda_produto': row[0], 'funcionario': row[1], 'produto': row[2]})
        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Edita item na Comanda - se zero exclui
@router.put("/comanda/item", tags=["Comanda"])
async def put_comanda_item(corpo: ComandaProdutos):
    try:
        session = db.Session()
        # busca os dados atuais do item selecionado da comanda

        dados = session.query(ComandaProdutoDB).filter(ComandaProdutoDB.id_comanda_produto == corpo.id_comanda_produto).one()
        # se nova quantidade zerada, exclui
        if (corpo.quantidade == 0):
            session.delete(dados)
        # edita
        else:
        # dados.comanda_id = corpo.comanda_id
        # dados.produto_id = corpo.produto_id
            dados.funcionario_id = corpo.funcionario_id
            dados.quantidade = corpo.quantidade
            dados.valor_unitario = corpo.valor_unitario
            session.add(dados)
            session.commit()

            return {"id": dados.id_comanda_produto}, 200
        
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()


# Retorna o total da comanda
@router.get("/comandas/{comanda_id}", tags=["Comanda"])
async def get_comanda_total(comanda_id: int):
    try:
        session = db.Session()

        from sqlalchemy.sql import func
        dados = session.query(func.sum(ComandaProdutoDB.quantidade * ComandaProdutoDB.valor_unitario).label(
            "Total:")).filter(ComandaProdutoDB.comanda_id == comanda_id).scalar()
        
        return {"total_comanda": dados}, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()