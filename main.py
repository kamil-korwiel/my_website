from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
from pathlib import Path

from model.know import Know 

def get_markdown(path:Path) -> str:
    try:
        with path.open('r', encoding='utf-8') as file:
            text = markdown.markdown(file.read(), extensions=['fenced_code', 'tables'])
    except Exception as e:
        text = '<h3 class="error">Error: Markdown file not found.</h3>'
    return text
    

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


markdown_path_about = Path("./data/index/about/about.md")

markdown_path_python = Path("./data/index/knowledge/python.md")
markdown_path_testing = Path("./data/index/knowledge/testing.md")
markdown_path_others = Path("./data/index/knowledge/others.md")

markdown_path_genkaraoke = Path("./data/index/projects/genkaraoke.md")
markdown_path_test = Path("./data/index/projects/testing.md")
markdown_path_scraping = Path("./data/index/projects/scraping.md")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    knows_short = [
        Know(
            name="Python",
            path_img="350px/Python-Blue-350.png",
            text=get_markdown(markdown_path_python)
        ),
        Know(
            name="Testing",
            path_img="350px/Test-Green-350.png",
            text=get_markdown(markdown_path_testing)
        ),
        Know(
            name="Other",
            path_img="350px/Linux-orange-350.png",
            text=get_markdown(markdown_path_others)
        ),
    ]

    projects_short = [
        get_markdown(markdown_path_genkaraoke),
        get_markdown(markdown_path_test),
        get_markdown(markdown_path_scraping),
    ]

    context = {
        "about": get_markdown(markdown_path_about),
        "knows": [know.__dict__ for know in knows_short],
        "projects": "\n".join(projects_short)
    }
    return templates.TemplateResponse(request=request, name="site/index.html", context=context)


@app.get("/projects", response_class=HTMLResponse)
async def my_music(request: Request):
    return templates.TemplateResponse(request=request, name="/card.html")

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(request=request, name="site/contact.html")

@app.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    return templates.TemplateResponse(request=request, name="site/blog.html")