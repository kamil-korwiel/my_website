from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
from pathlib import Path 



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    html = ""
    markdown_path_about_long = Path("./data/about.md")
    markdown_path_about_short = Path("./data/about-short.md")

    try:
        with markdown_path_about_long.open('r', encoding='utf-8') as file:
            text_md = file.read()
            about_long = markdown.markdown(text_md, extensions=['fenced_code', 'tables'])

        with markdown_path_about_short.open('r', encoding='utf-8') as file:
            text_md = file.read()
            about_short = markdown.markdown(text_md, extensions=['fenced_code', 'tables'])
    except FileNotFoundError:
        about_short = about_long = "<p>Error: Markdown file not found.</p>"
    
    return templates.TemplateResponse(request=request, name="site/index.html", context={ "about_long" : about_long, "about_short": about_short })


@app.get("/music-i-listen", response_class=HTMLResponse)
async def my_music(request: Request):
    return templates.TemplateResponse(request=request, name="site/top-names.html",)

@app.get("/notes", response_class=HTMLResponse)
async def my_music(request: Request):
    return templates.TemplateResponse(request=request, name="card.html",)