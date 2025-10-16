from pydantic import BaseModel
from typing import Optional
from datetime import date

#Vai facilitar a entrada de informações no banco de dados, e deixar mais customizável
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    saldo: float
    admin: Optional[bool]
    
    class Config:
        from_attributes = True
    
class LoginSchema(BaseModel):
    email: str
    senha: str    

    class Config:
        from_attributes = True
    
class TransacaoSchema(BaseModel):
    tipo: str
    valor: float
    categoria: str #Categorias de gasto, Ex.: Lazer, Comida, Esporte
    descricao: Optional[str]       

    class Config:
        from_attributes = True
        
class EditarSchema(BaseModel):
    categoria: str #Categorias de gasto, Ex.: Lazer, Comida, Esporte
    descricao: Optional[str]       

    class Config:
        from_attributes = True        

class RespostaSchema(BaseModel):
    id: int
    tipo: str
    categoria: str
    valor: float
    data: date

    class Config:
        from_attributes = True    

class RespostaCategoriaSchema(BaseModel):
    categoria: str
    valor: float

    class Config:
        from_attributes = True

class ResumoSchema(BaseModel):
    ENTRADA: list[RespostaCategoriaSchema]
    SAÍDA: list[RespostaCategoriaSchema]                        