from fastapi import APIRouter
from domain.entities.Funcionario import Funcionario

# import da persistência
import db
from infra.orm.FuncionarioModel import FuncionarioDB

# import da segurança
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

router = APIRouter()

# Criar as rotas/endpoints: GET, POST, PUT, DELETE
@router.get("/funcionario/", tags=["Funcionário"])
async def get_funcionario():
    try:
        session = db.Session()

        # busca todos
        dados = session.query(FuncionarioDB).all()
        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/{id}", tags=["Funcionário"])
async def get_funcionario(id: int,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()

        # busca um com filtro
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).all()

        print(current_user)

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/funcionario/", tags=["Funcionário"])
async def post_funcionario(corpo: Funcionario,current_user:Annotated[User, Depends(get_current_active_user)],):
  try:
        session = db.Session()
    
       # Ajuste aqui: use a classe FuncionarioDB sem o id_funcionario
        dados = FuncionarioDB(
            nome=corpo.nome,
            matricula=corpo.matricula,
            cpf=corpo.cpf,
            telefone=corpo.telefone,
            grupo=corpo.grupo,
            senha=corpo.senha
        )

        session.add(dados)
        session.commit()

        print(current_user)

        # Retorne o id do funcionário recém-criado
        return {"id": dados.id_funcionario}, 200

  except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
  finally:
        session.close()

@router.put("/funcionario/{id}", tags=["Funcionário"])
async def put_funcionario(id: int, corpo: Funcionario,current_user:Annotated[User, Depends(get_current_active_user)]):
    try:
        session = db.Session()
        # busca os dados atuais pelo id

        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        # atualiza os dados com base no corpo da requisição
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        dados.senha = corpo.senha
        dados.matricula = corpo.matricula
        dados.grupo = corpo.grupo

        session.add(dados)
        session.commit()

        print(current_user)

        return {"id": dados.id_funcionario}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/funcionario/{id}", tags=["Funcionário"])
async def delete_funcionario(id: int,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()

        # busca os dados atuais pelo id
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        session.delete(dados)
        session.commit()

        print(current_user)

        return {"id": dados.id_funcionario}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# valida o cpf e senha informado pelo usuário
@router.post("/funcionario/login/", tags=["Funcionário - Login"])
async def login_funcionario(corpo: Funcionario,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()

        # one(), requer que haja apenas um resultado no conjunto de resultados
        # é um erro se o banco de dados retornar 0, 2 ou mais resultados e uma exceção será gerada
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == corpo.cpf).filter(FuncionarioDB.senha == corpo.senha).one()

        print(current_user)

        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# verifica se o CPF informado já esta cadastrado, retornado os dados atuais caso já esteja
@router.get("/funcionario/cpf/{cpf}", tags=["Funcionário - Valida CPF"])
async def cpf_funcionario(cpf: str,current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = db.Session()

        # busca um com filtro, retornando os dados cadastrados
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == cpf).all()

        print(current_user)
        
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
     session.close()