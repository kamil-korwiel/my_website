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
    markdown_path = Path("./data/about.md")

    try:
        with markdown_path.open('r', encoding='utf-8') as file:
            text_md = file.read()
            html = markdown.markdown(text_md, extensions=['fenced_code', 'tables'])
    except FileNotFoundError:
        html = "<p>Error: Markdown file not found.</p>"
    
    return templates.TemplateResponse(request=request, name="site/index.html", context={"html" : html})


@app.get("/music-i-listen", response_class=HTMLResponse)
async def my_music(request: Request):
    return templates.TemplateResponse(request=request, name="errors/work_in_progress.html",)