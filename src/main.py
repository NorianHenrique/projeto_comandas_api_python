from fastapi import FastAPI
from settings import HOST, PORT, RELOAD
import uvicorn

# import das classes com as rotas/endpoints
import security
from app import FuncionarioDAO
from app import ClienteDAO
from app import ProdutoDAO
from app import ComandaDAO

from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # executa no startup
    print("API has started")

    # cria, caso não existam, as tabelas de todos os modelos que encontrar na aplicação (importados)
    import db
    await db.criaTabelas()

    yield
    
    # executa no shutdown
    print("API is shutting down")

# cria a aplicação FastAPI com o contexto de vida
app = FastAPI(lifespan=lifespan)

# rota padrão
@app.get("/")
async def root():
    return {"detail": "API Comandas", "Swagger UI": "http://127.0.0.1:8000/docs", "ReDoc":
    "http://127.0.0.1:8000/redoc"}

# mapeamento das rotas/endpoints
app.include_router(security.router)
app.include_router(FuncionarioDAO.router)
app.include_router(ClienteDAO.router)
app.include_router(ProdutoDAO.router)
app.include_router(ComandaDAO.router)


if __name__ == "__main__":
    import ssl
    import hypercorn.asyncio
    from hypercorn.config import Config
    import asyncio

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="cert/cert.pem", keyfile="cert/ecc-key.pem")

    config = Config()
    config.bind = ["0.0.0.0:4443"]
    config.quic_bind = ["0.0.0.0:4443"]
    #config.insecure_bind = ["0.0.0.0:8000"]
    config.certfile = "cert/cert.pem"
    config.keyfile = "cert/ecc-key.pem"
    config.alpn_protocols = ["h2","h3"]
    
    asyncio.run(hypercorn.asyncio.serve(app, config))