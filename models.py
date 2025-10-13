from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, DateTime, func, Date
import datetime
from sqlalchemy.orm import declarative_base

#Data atual ( o do sqlalchemy não prestou pro meu uso )
agora = datetime.datetime.now()
data_atual = agora.date()

#Cria o banco de dados
db = create_engine('sqlite:///banco.db')
base = declarative_base()

#Essa classe vai passar as informações necessárias para salvar os usuário no  Banco de dados
class Usuario(base):
    __tablename__ = 'usuarios'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String)
    email = Column('email', String, nullable=False)
    senha = Column('senha', String)
    saldo = Column('saldo', Float, default=0)
    admin = Column('admin', Boolean, default=False)
    
    def __init__(self, nome, email, senha, saldo = 0, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.saldo = saldo
        self.admin = admin

#Essa classe vai salvar as transações do usuário
class Transacao(base):
    __tablename__ = 'transacoes'
   
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    usuario_id = Column('usuario_id', Integer, ForeignKey('usuarios.id'))
    tipo = Column('tipo', String) #Vai ser ENTRADA ou SAÍDA!
    valor = Column('valor', Float)
    categoria = Column('categoria', String) #Categorias de gasto, Ex.: Lazer, Comida, Esporte
    data = Column(Date)
    descricao = Column('descricao', String) #Descricao da compra, opcional   
    
    def __init__(self, usuario_id, tipo, valor, categoria, descricao, data = data_atual):
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.valor = valor
        self.categoria = categoria
        self.data = data
        self.descricao = descricao

        