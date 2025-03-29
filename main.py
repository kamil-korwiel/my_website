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


markdown_path_about_short = Path("./data/about/about_short.md")

markdown_path_python_short = Path("./data/knowledge/python_short.md")
markdown_path_testing_short = Path("./data/knowledge/testing_short.md")
markdown_path_others_short = Path("./data/knowledge/others_short.md")

markdown_path_genkaraoke_short = Path("./data/projects/genkaraoke_short.md")
markdown_path_test_short = Path("./data/projects/testing_short.md")
markdown_path_scraping_short = Path("./data/projects/scraping_short.md")


markdown_path_about_long = Path("./data/about/about_long.md")

markdown_path_python_long = Path("./data/knowledge/python_long.md")
markdown_path_testing_long = Path("./data/knowledge/testing_long.md")
markdown_path_others_long = Path("./data/knowledge/others_long.md")

markdown_path_genkaraoke_long = Path("./data/projects/genkaraoke_long.md")
markdown_path_test_long = Path("./data/projects/testing_long.md")
markdown_path_scraping_long = Path("./data/projects/scraping_long.md")



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):

    knows_long = [
        Know(
            name="Python",
            path_img="350px/Python-Blue-350.png",
            text=get_markdown(markdown_path_python_long)
        ),
        Know(
            name="Testing",
            path_img="350px/Test-Green-350.png",
            text=get_markdown(markdown_path_testing_long)
        ),
        Know(
            name="Other",
            path_img="350px/Linux-orange-350.png",
            text=get_markdown(markdown_path_others_long)
        ),
    ]
    knows_short = [
        Know(
            name="Python",
            path_img="350px/Python-Blue-350.png",
            text=get_markdown(markdown_path_python_short)
        ),
        Know(
            name="Testing",
            path_img="350px/Test-Green-350.png",
            text=get_markdown(markdown_path_testing_short)
        ),
        Know(
            name="Other",
            path_img="350px/Linux-orange-350.png",
            text=get_markdown(markdown_path_others_short)
        ),
    ]
    
    projects_long = [
        get_markdown(markdown_path_genkaraoke_long),
        get_markdown(markdown_path_test_long),
        get_markdown(markdown_path_scraping_long),
    ]

    projects_short = [
        get_markdown(markdown_path_genkaraoke_short),
        get_markdown(markdown_path_test_short),
        get_markdown(markdown_path_scraping_short),
    ]

    context = {
        "short":{
            "about": get_markdown(markdown_path_about_short),
            "knows": [know.__dict__ for know in knows_short],
            "projects": "\n".join(projects_short)
            
        },
        "long": {
            "about": get_markdown(markdown_path_about_long),
            "knows": [know.__dict__ for know in knows_long],
            "projects": "\n".join(projects_long)
        }
    }
    return templates.TemplateResponse(request=request, name="site/index.html", context=context)


@app.get("/cool-music", response_class=HTMLResponse)
async def my_music(request: Request):
    return templates.TemplateResponse(request=request, name="errors/work_in_progress.html")

@app.get("/notes", response_class=HTMLResponse)
async def my_music(request: Request):
    return templates.TemplateResponse(request=request, name="errors/work_in_progress.html")