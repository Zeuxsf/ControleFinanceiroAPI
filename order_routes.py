from fastapi import APIRouter, Depends, HTTPException
from schemas import TransacaoSchema, RespostaSchema, EditarSchema, RespostaCategoriaSchema, ResumoSchema
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from dependencies import pegar_sessao, verificar_token
from models import Transacao, Usuario
from typing import List


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

#Vai editar as transações. Eu deixei o usuário editar apenas as coisas mais supérfluas porque os outros dados eu considero importantes o suficiente para querer que ele crie uma nova transação. 
@order_router.put('/editar_transacao')
async def editar_transacao(id_da_transacao: int ,editar_schema: EditarSchema,session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    transacao_editada = session.query(Transacao).filter(Transacao.id==id_da_transacao).first()
    if not transacao_editada:
        raise HTTPException(status_code=401, detail='Essa transação não existe.')
    elif usuario.id != transacao_editada.usuario_id:
        raise HTTPException(status_code=401, detail='Você não é dono dessa transação.')
    else:
        transacao_editada.categoria = editar_schema.categoria
        transacao_editada.descricao = editar_schema.descricao
        
    session.add(transacao_editada)
    session.commit()
    
    return {'mensagem': f'Transação de ID {transacao_editada.id} atualizada com sucesso!'}

#Vai deletar as transações
@order_router.delete('/excluir_transacao')
async def excluir_transacao(id_da_transacao: int ,session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    transacao_deletada = session.query(Transacao).filter(Transacao.id==id_da_transacao).first()
    if not transacao_deletada:
        raise HTTPException(status_code=401, detail='Essa transação não existe.')
    elif usuario.id != transacao_deletada.usuario_id:
        raise HTTPException(status_code=401, detail='Você não é dono dessa transação.')
        
    session.delete(transacao_deletada)
    session.commit()
    
    return {'mensagem': f'Transação de ID {id_da_transacao} deletada com sucesso!'}


#Retorna total de SAÍDA e ENTRADA
@order_router.get('/soma_de_gastos')
async def soma_de_gastos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    total_entrada = session.query(func.sum(Transacao.valor)).filter(Transacao.usuario_id==usuario.id,Transacao.tipo=='ENTRADA').scalar()

    total_saida = session.query(func.sum(Transacao.valor)).filter(Transacao.usuario_id==usuario.id,Transacao.tipo=='SAÍDA').scalar()
    
    return {
        'ENTRADA': total_entrada,
        'SAÍDA': total_saida
    }    
    
 
#Estatísticas por categoria
@order_router.get('/gastos_por_categoria', response_model=ResumoSchema)
async def gastos_por_categoria(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    def resumo_por_categoria(tipo: str):
        resultados = (session.query(Transacao.categoria,func.sum(Transacao.valor).label("total")).filter(Transacao.usuario_id == usuario.id, Transacao.tipo == tipo).group_by(Transacao.categoria).order_by(desc(func.sum(Transacao.valor))).all())
        
        resumo = [{"categoria": r.categoria, "valor": float(r.total)} for r in resultados]
        return resumo

    total_entrada = resumo_por_categoria('ENTRADA')
    total_saida = resumo_por_categoria('SAÍDA')
    
    return {
        'ENTRADA': total_entrada,
        'SAÍDA': total_saida
    }