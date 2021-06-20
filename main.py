import logging

import yaml
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.embed import embed
from src.session import SessionManager
from src.initialize import TikTok

logger = logging.getLogger(__name__)

with open("config/config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


app = FastAPI()
logger.info("Initialized app")

app.mount(
    config["app"]["static_folder"],
    StaticFiles(directory="static"),
    name="static",
)
session = SessionManager(config["app"]["db_path"])

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Index page"""
    logger.info("Accessed main page")

    # Render template with the embedding
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/boot")
async def html_element():
    """Returning the most recent videos"""
    no_videos = config["app"]["num_tiktoks"]
    logger.debug("Loading %i videos", no_videos)
    initial = session.get_latest(no_videos)

    # Get embedding code for each video as a list
    embeds = await embed(initial)
    logger.debug("Returning %i videos", len(initial))

    # Return embedding code as a list
    return embeds


@app.post("/newembed")
async def post_link(request: Request):
    """Post new link to database"""
    link = await request.json()
    logger.info(
        "Received new insertion request: %s, %i",
        link["shortlink"],
        link["timestamp"],
    )
    session.add_to_db(
        TikTok(shortlink=link["shortlink"], timestamp=link["timestamp"])
    )
    
    return "success"
