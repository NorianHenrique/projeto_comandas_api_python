from pydantic import BaseModel
from datetime import date

class Comanda(BaseModel):
    id_comanda: int = None
    comanda: str
    data_hora: date
    status: int
    cliente_id: int = None
    funcionario_id: int 

class ComandaProdutos(BaseModel):
    id_comanda_produto: int = None
    comanda_id: int  # Anotação correta
    produto_id: int  # Anotação correta
    funcionario_id: int  # Anotação correta
    quantidade: int
    valor_unitario: float