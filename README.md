
# API de Comandas

Uma API robusta desenvolvida para gerenciar comandas de um estabelecimento, permitindo controle eficiente dos pedidos, itens e status das comandas. Ideal para sistemas de frente de caixa, restaurantes, bares e outros negócios que necessitam de um controle dinâmico de consumo.

## Status do Projeto

Em desenvolvimento

## ✨ Funcionalidades

* **Gerenciamento de Clientes:**
    * Criação, leitura, atualização e exclusão (CRUD) de clientes.
    * Validação de CPF para evitar duplicidade.
* **Gerenciamento de Funcionários:**
    * CRUD de funcionários.
    * Autenticação de funcionários com login por CPF e senha.
    * Controle de acesso por grupo.
* **Gerenciamento de Produtos:**
    * CRUD de produtos.
    * Validação de nome de produto para evitar duplicidade.
    * Inclusão de descrição, foto e valor unitário.
* **Gerenciamento de Comandas:**
    * Abertura, edição, fechamento e cancelamento de comandas.
    * Adição e remoção de itens em comandas.
    * Cálculo do valor total da comanda.
    * Associação de comandas a clientes e funcionários.
* **Autenticação JWT:** Proteção das rotas da API com tokens JWT.

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **FastAPI:** Framework web de alta performance para construção da API.
* **SQLAlchemy:** ORM (Object Relational Mapper) para interação com o banco de dados.
* **PyMySQL:** Driver para conexão com bancos de dados MySQL (utilizado na configuração via Docker Compose).
* **SQLite:** Banco de dados padrão para desenvolvimento local se não usar Docker.
* **Docker:** Para conteinerização da aplicação e do banco de dados.
* **Docker Compose:** Para orquestração dos contêineres da aplicação e do banco de dados.
* **`python-dotenv`**: Para gerenciamento de variáveis de ambiente.
* **`passlib`**: Para hashing de senhas.
* **`python-jose`**: Para manipulação de tokens JWT.
