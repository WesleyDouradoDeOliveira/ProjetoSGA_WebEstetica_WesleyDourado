from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="ProjetoSGA_WebEstetica_WesleyDourado",
    description="API para Sistema de Gestão e Agendamento Estético - Rose Dourado Estética",
    version="1.0.0"
)

# Servir arquivos estáticos (Front-end)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelos de Dados (Pydantic)
class AgendamentoCreate(BaseModel):
    nome_cliente: str
    telefone: str
    procedimento: str
    data: str
    horario: str

class AgendamentoResponse(AgendamentoCreate):
    id: int
    status: str
    sessao_pacote: str

# Banco de dados simulado em memória
db_agendamentos: List[dict] = [
    {
        "id": 1,
        "nome_cliente": "Ana Souza",
        "telefone": "(11) 98888-7777",
        "procedimento": "Drenagem Pós-Operatória",
        "data": "2026-10-25",
        "horario": "14:00",
        "status": "agendado",
        "sessao_pacote": "3/10"
    }
]

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/agendamentos", response_model=List[AgendamentoResponse])
def listar_agendamentos():
    return db_agendamentos

@app.post("/api/agendamentos", response_model=AgendamentoResponse, status_code=201)
def criar_agendamento(item: AgendamentoCreate):
    # Validação simples de conflito de horário
    for ag in db_agendamentos:
        if ag["data"] == item.data and ag["horario"] == item.horario and ag["status"] == "agendado":
            raise HTTPException(status_code=400, detail="Este horário já está ocupado. Escolha outro horário.")
    
    novo_id = len(db_agendamentos) + 1
    novo_agendamento = {
        "id": novo_id,
        "nome_cliente": item.nome_cliente,
        "telefone": item.telefone,
        "procedimento": item.procedimento,
        "data": item.data,
        "horario": item.horario,
        "status": "agendado",
        "sessao_pacote": "1/10"
    }
    db_agendamentos.append(novo_agendamento)
    return novo_agendamento