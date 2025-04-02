from datetime import datetime
import os
from pathlib import Path
from loguru import logger
import markdown
from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, select

from model.blog import Blog

import json

def get_json_data(path:Path):
    if path.exists():
        logger.debug(f"Get JSON file: '{path}'")
        with path.open("r") as file:
            json_text = file.read()
            return json_text
    else:
        logger.debug(f"No JSON file: '{path}'")


def get_markdown(path:Path) -> str:
    try:
        with path.open('r', encoding='utf-8') as file:
            text = markdown.markdown(file.read(), extensions=['fenced_code', 'tables'])
    except Exception as e:
        text = '<h3 class="error">Error: Markdown file not found.</h3>'
    return text



# DataBase
def init_db(engine:Engine, name_file:str) -> None:
    # Check if the database file exists
    db_exists = os.path.exists(name_file)

    # Create tables only if they don't exist
    if not db_exists:
        logger.info("Initializing database...")
        SQLModel.metadata.create_all(engine)
        # blog_json = get_json_data(Path('./data/blogs.json'))
        # load_blog_data_to_db(engine,blog_json)
    else:
        logger.info("Database already exists, skipping initialization.")
        # blog_json = get_json_data(Path('./data/blogs.json'))
        # insert_blog_data_to_db(engine,blog_json)

def convert_to_id(str:str):
        return str.strip().replace(" ","_").lower()
    
def load_blog_data_to_db(engine:Engine,json_str:str) -> None:
    
    json_blogs:dict[str,str] = json.loads(json_str)
    date_format = "%d.%m.%Y"
    blogs:list[Blog] = [
        Blog(
            id=convert_to_id(blog['title']),
            title=blog['title'],
            date=datetime.strptime(blog['date'], date_format),
            file_md_path=blog['file_md_path']
        ) for blog in json_blogs
    ]
    
    logger.info("Loading a data for JSON to DATABASE.")
    with Session(engine) as session:
        session.add_all(blogs)
        session.commit()

def insert_blog_data_to_db(engine:Engine,json_str:str):

    with Session(engine) as session:
        statement = select(Blog.id)
        id_blogs = session.exec(statement).all()
    
    json_blogs:dict[str,str] = json.loads(json_str)
    date_format = "%d.%m.%Y"
    # Check is new record in JSON
    new_blogs = set([convert_to_id(blog['title']) for blog in json_blogs]).difference(set(id_blogs))
    if new_blogs:
        logger.debug("Inserting a data for JSON to DATABASE.")
        blogs:list[Blog] = [
            Blog(
                id=convert_to_id(json_blogs),
                title=blog['title'],
                date=datetime.strptime(blog['date'], date_format),
                file_md_path=blog['file_md_path']
            )
            for blog in json_blogs
            if blog['title'] in new_blogs
        ]
        with Session(engine) as session:
            session.add_all(blogs)
            session.commit()
    else:
        logger.debug("Nothing new to insert to DATABASE.")

# ! Need for rethinking
def sync_blog_data_to_db(engine:Engine,json_str:str):

    with Session(engine) as session:
        statement = select(Blog)
        blogs_db = session.exec(statement).all()
    
    blogs_json:dict[str,str] = json.loads(json_str)
    date_format = "%d.%m.%Y"
    
    # Check is new record in JSON
    
    
    
    # if new_blogs:
    #     logger.debug("Inserting a data for JSON to DATABASE.")
    #     blogs:list[Blog] = [
    #         Blog(
    #             id=convert_to_id(blogs_json),
    #             title=blog['title'],
    #             date=datetime.strptime(blog['date'], date_format),
    #             file_md_path=blog['file_md_path']
    #         )
    #         for blog in blogs_json
    #         if blog['title'] in new_blogs
    #     ]
    #     with Session(engine) as session:
    #         session.add_all(blogs)
    #         session.commit()
    # else:
    #     logger.debug("Nothing new to insert to DATABASE.")

        

    


    
