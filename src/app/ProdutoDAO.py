from fastapi import APIRouter, HTTPException
from domain.entities.Produto import Produto

import db
from infra.orm.ProdutoModel import ProdutoDB

# import da segurança
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

router = APIRouter()

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

@router.get("/produto/", tags=["Produto"])
async def get_produto():
    try:
        session = db.Session()
        # Busca todos os produtos
        dados = session.query(ProdutoDB).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/produto/{id}", tags=["Produto"])
async def get_produto(id: int,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()
        # Busca um produto específico pelo ID
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()  # espera um único resultado

        print(current_user)

        return dados, 200
    except Exception as e:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    finally:
        session.close()

@router.post("/produto/", tags=["Produto"])
async def post_produto(corpo: Produto,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()
        
        # Verifica se já existe um produto com o mesmo nome
        produto_existente = session.query(ProdutoDB).filter(ProdutoDB.nome == corpo.nome).first()
        if produto_existente:
            raise HTTPException(status_code=400, detail="Produto com o mesmo nome já cadastrado")

        # Cria um novo objeto com os dados da requisição
        dados = ProdutoDB(None, corpo.nome, corpo.descricao, corpo.foto, corpo.valor_unitario)
        session.add(dados)
        session.commit()

        print(current_user)
        
        return {"id": dados.id_produto}, 201  # Retorna o id do produto criado
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/produto/{id}", tags=["Produto"])
async def put_produto(id: int, corpo: Produto,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()

        # Busca os dados atuais pelo ID
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()

        # Atualiza os dados com base no corpo da requisição
        dados.nome = corpo.nome
        dados.descricao = corpo.descricao
        dados.foto = corpo.foto
        dados.valor_unitario = corpo.valor_unitario

        session.add(dados)
        session.commit()

        print(current_user)
        
        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/produto/{id}", tags=["Produto"])
async def delete_produto(id: int,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()

        # Busca os dados atuais pelo ID
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        session.delete(dados)
        session.commit()

        print(current_user)

        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Verifica se o nome do produto informado já está cadastrado, retornando os dados atuais caso já esteja
@router.get("/produto/nome/{nome}", tags=["Produto - Valida Nome"])
async def nome_produto(nome: str,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()

        # Busca um produto pelo nome
        dados = session.query(ProdutoDB).filter(ProdutoDB.nome == nome).all()

        print(current_user)
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()
