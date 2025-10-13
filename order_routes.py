from fastapi import APIRouter, Depends, HTTPException
from schemas import TransacaoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Transacao, Usuario

order_router = APIRouter(prefix='/order', tags=['Transação'])

@order_router.post('/criar_transacao')
async def criar_transacao(transacao_schema: TransacaoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    nova_transacao = Transacao(usuario.id, transacao_schema.tipo, transacao_schema.valor, transacao_schema.categoria, transacao_schema.descricao)
    
   # if usuario.id != nova_transacao.usuario_id:
    #    raise HTTPException(status_code=401, detail='Você não pode atribuir suas dívidas a outros!')
    
    session.add(nova_transacao)
    session.commit()
    
    return {'mensagem': f'Transação da categoria {transacao_schema.categoria}, no valor de {transacao_schema.valor} concluída com sucesso!'}