from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import random
import string

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_password", response_class=HTMLResponse)
async def generate_password(request: Request):
    form_data = await request.form()
    length = form_data.get("length")
    if length is not None and length.isdigit():
        length = int(length)
    else:
        length = 8  # default length
    uppercase = form_data.get("uppercase")
    lowercase = form_data.get("lowercase")
    characters = string.digits  # добавляем цифры
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase or characters == '':
        characters += string.ascii_lowercase
    password = ''.join(random.choice(characters) for i in range(length))
    return templates.TemplateResponse("index.html", {"request": request, "password": password})
