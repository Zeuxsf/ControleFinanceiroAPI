from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from main import oauth2_schema,SECRET_KEY,ALGORITHM,ACCESS_TOKEN_TIME

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()    
        
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dict_info.get('sub'))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f'Acesso inválido. {e}')
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:    
        raise HTTPException(status_code=401, detail='Acesso inválido.')
    return usuario        