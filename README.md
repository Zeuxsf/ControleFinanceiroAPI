# Controle Financeiro - API


> API completa para controle financeiro pessoal — com autenticação segura, CRUD de transações e endpoints adicionais para análise de gastos.

---

📖 Sobre o projeto

Este é o meu primeiro projeto de API desenvolvido de forma independente.
Ela foi criada com FastAPI (Python) e tem como objetivo gerenciar finanças pessoais, permitindo registrar, visualizar e editar transações, além de autenticação segura com bcrypt e JWT.

A API está totalmente funcional e pronta para integração com um front-end.

---

🚀 Funcionalidades principais

🔐 Autenticação

POST /auth/registrar → Cria novo usuário (senha criptografada com bcrypt)

POST /auth/login → Login com retorno de token JWT

POST /auth/login_form → Login via formulário

GET /auth/refresh → Atualiza o token de autenticação


💸 Transações

POST /order/alterar_saldo → Altera o saldo do usuário

POST /order/criar_transacao → Cria nova transação (Entrada/Saída)

GET /order/visualizar_transacoes → Lista todas as transações

PUT /order/editar_transacao → Edita transação existente

DELETE /order/excluir_transacao → Exclui transação

GET /order/soma_de_gastos → Retorna soma total de gastos

GET /order/gastos_por_categoria → Mostra gastos agrupados por categoria



---

🧠 Tecnologias utilizadas

Python 3.10+

FastAPI — framework principal

Uvicorn — servidor ASGI

bcrypt — criptografia de senhas

JWT (PyJWT) — autenticação

SQLAlchemy / SQLite — banco de dados e ORM



---

⚙️ Como rodar o projeto localmente

1. Clone o repositório:



git clone https://github.com/seu-usuario/controle-financeiro-api.git
cd controle-financeiro-api

2. Crie e ative um ambiente virtual:



python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

3. Instale as dependências:



pip install -r requirements.txt

4. Crie um arquivo .env com suas configurações:



SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

5. Inicie o servidor:



uvicorn app.main:app --reload

6. Acesse a documentação interativa (Swagger UI):



http://localhost:8000/docs

---

📊 Exemplos de uso (Swagger UI)



A documentação interativa permite testar todos os endpoints facilmente, com suporte a autenticação via token JWT.

---

🧾 Licença

Este projeto é distribuído sob a licença MIT.
Sinta-se à vontade para usar, modificar e contribuir!


---

*Criado por: Alexandre S. de França*


