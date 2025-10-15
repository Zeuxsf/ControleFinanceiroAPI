from fastapi import APIRouter, Depends, HTTPException
from schemas import TransacaoSchema, RespostaSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Transacao, Usuario
from typing import List, Optional


order_router = APIRouter(prefix='/order', tags=['Transação'])

#Você adiciona ou retira seu saldo disponível
@order_router.post('/alterar_saldo')
async def alterar_saldo(tipo_de_transacao: str, novo_saldo: int,session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    if tipo_de_transacao == 'ENTRADA':
        usuario.saldo += novo_saldo
    elif tipo_de_transacao == 'SAÍDA':
        usuario.saldo -= novo_saldo        
    
    session.add(usuario)
    session.commit()
    
    return {'mensagem': f'Saldo alterado com sucesso.'}

#Vai criar uma transação
@order_router.post('/criar_transacao')
async def criar_transacao(transacao_schema: TransacaoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    nova_transacao = Transacao(usuario.id, transacao_schema.tipo, transacao_schema.valor, transacao_schema.categoria, transacao_schema.descricao)
    if nova_transacao.tipo == 'SAÍDA':
        usuario.saldo -= nova_transacao.valor
    elif nova_transacao.tipo == 'ENTRADA':
        usuario.saldo += nova_transacao.valor
    
    session.add(nova_transacao)
    session.commit()

    if usuario.saldo == 0 or usuario.saldo < 0:
        return {'mensagem': f'Transação da categoria {transacao_schema.categoria}, no valor de R${transacao_schema.valor} concluída com sucesso. Seu saldo acabou ou/e está no negativo.'}    
    
    return {'mensagem': f'Transação da categoria {transacao_schema.categoria}, no valor de R${transacao_schema.valor} concluída com sucesso!'}

#Vai visualizar todas as transações, e o usuário vai poder escolher por categoria e tipo (do usuário logado. Decidi não criar uma função pra ver de todos os usuarios de uma vez, achei desnecessário)
@order_router.get('/visualizar_transacoes', response_model=List[RespostaSchema])
async def visualizar_transacoes(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token), tipo: str = None, categoria: str = None):
  
    if tipo == None and categoria == None:
        transacoes = session.query(Transacao).filter(Transacao.usuario_id==usuario.id).all()
    elif tipo == None:
        transacoes = session.query(Transacao).filter(Transacao.usuario_id==usuario.id, Transacao.categoria==categoria).all()
    elif categoria == None:    
        transacoes = session.query(Transacao).filter(Transacao.usuario_id==usuario.id, Transacao.tipo == tipo).all()
    else:
        transacoes = session.query(Transacao).filter(Transacao.usuario_id==usuario.id, Transacao.tipo == tipo, Transacao.categoria==categoria).all()              
    return transacoes

#Vai editar as transações

#Vai deletar as transações

#Retorna total de SAÍDA e ENTRADA
 
#Estatísticas por categoria/mês 