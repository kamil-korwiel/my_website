from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException


templates = Jinja2Templates(directory='templates')



async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse('error/404.html', {'request': request}, status_code=404)


# async def internal_error(request: Request, exc: HTTPException):
#     return templates.TemplateResponse('500.html', {'request': request}, status_code=500)

    


exception_handlers = {
    404: not_found_error,
}