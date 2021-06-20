from re import template
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.embed import embed
from src.session import SessionManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
session = SessionManager("sqlite:///clean.db")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    initial = session.get_latest(10)

    embeds = await embed(initial)

    return templates.TemplateResponse(
        "index.html", {"request": request, "embeds": embeds}
    )


@app.get("/boot")
async def html_element():
    initial = session.get_latest(10)

    embeds = await embed(initial)

    return embeds

@app.post("/newembed")
async def post_link(request: Request):
    pass