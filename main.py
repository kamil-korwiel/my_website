from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from errors import exception_handlers
from sqlmodel import Session, create_engine, select
import json
from model.blog import Blog
from model.know import Know
from utilities import get_json_data, get_markdown, init_db, insert_blog_data_to_db

    
# Initializing  application 
app = FastAPI(exception_handlers=exception_handlers)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initializing  database 
engine = create_engine("sqlite:///database.db")
init_db(engine,Path('./database.db'))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    markdown_path_about = Path("./data/index/about/about.md")

    knows_json = get_json_data(Path("./data/index/know.json"))
    knows = [
        {
            'name': know['name'],
            'path_img': Path(know['path_img']),
            'text': get_markdown(Path(know['path_md']))
        } for know in json.loads(knows_json)
    ]

    projects_json = get_json_data(Path("./data/index/projects.json"))
    projects = [
       get_markdown(Path(pro_path)) for pro_path in json.loads(projects_json)
    ]

    context = {
        "about": get_markdown(markdown_path_about),
        "knows": knows,
        "projects": "\n".join(projects)
    }
    return templates.TemplateResponse(request=request, name="site/index.html", context=context)


@app.get("/projects", response_class=HTMLResponse)
async def my_music(request: Request):
    return templates.TemplateResponse(request=request, name="/card.html")

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(request=request, name="site/contact.html")

@app.get("/blogs", response_class=HTMLResponse)
async def blog(request: Request):
    with Session(engine) as session:
        statement = select(Blog)
        results = session.exec(statement).all()
        
        formatted_results = [
            {
                "id": blog.id,
                "title": blog.title,
                "date": blog.date.strftime("%d.%m.%Y") 
            }
            for blog in results
        ]

    return templates.TemplateResponse(request=request, name="site/blogs.html",context={"blogs" : formatted_results})

@app.get("/blog/{id}", response_class=HTMLResponse)
async def blog(id: str, request: Request):
    try:
        with Session(engine) as session:
            blog = session.get(Blog, id)
            md_text = get_markdown(Path(blog.file_md_path))
        return templates.TemplateResponse(request=request, name="site/blog.html",context={"md_blog": md_text})
    except Exception as e:
        raise HTTPException(status_code=404)
    

    
