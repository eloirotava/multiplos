from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import os
from typing import Dict, List

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="sua-chave-secreta-aqui")

templates = Jinja2Templates(directory="templates")

DB_DIR = "dbs"

# Simulação de banco de dados de usuários
USERS_DB: Dict[str, Dict[str, str]] = {
    "restaurante1": {"password": "senha123", "db_file": "restaurante1.db"},
    "restaurante2": {"password": "senha456", "db_file": "restaurante2.db"},
}

# Dependência para obter o caminho do DB da sessão
def get_db_path(request: Request):
    db_file = request.session.get("db_file")
    if not db_file:
        raise HTTPException(status_code=401, detail="Você não está logado.")
    db_path = os.path.join(DB_DIR, db_file)
    if not os.path.exists(db_path):
        raise HTTPException(status_code=500, detail="Banco de dados do cliente não encontrado.")
    return db_path

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if "db_file" in request.session:
        return RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=RedirectResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user_info = USERS_DB.get(username)

    if user_info and user_info["password"] == password:
        request.session["db_file"] = user_info["db_file"]
        return RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@app.get("/logout", response_class=RedirectResponse)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

# Rota para a página principal
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, db_path: str = Depends(get_db_path)):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT item, preco FROM menu")
    menu_items = cursor.fetchall()
    conn.close()

    # Formata os dados para o template
    menu_list = [{"item": item, "preco": f"R$ {preco:.2f}"} for item, preco in menu_items]
    
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "username": request.session["db_file"].replace(".db", ""), "menu_items": menu_list}
    )