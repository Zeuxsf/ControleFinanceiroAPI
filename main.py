from fastapi import FastAPI
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

#Senhas criptografadas
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

#JWT tokens
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_TIME = int(os.getenv('ACCESS_TOKEN_TIME'))

#Ativar formulario de login na docs
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login_form')

#Roteadores de rota
from auth_routes import auth_router
from order_routes import order_router

app = FastAPI() #Cria o app
app.include_router(auth_router)
app.include_router(order_router)
#end