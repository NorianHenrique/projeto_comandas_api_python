from pydantic import BaseModel

class Funcionario(BaseModel):
    id_funcionario: int = None
    nome: str
    matricula: str
    cpf: str
    telefone: str = None
    grupo: int
    senha: str = None