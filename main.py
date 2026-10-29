from fastapi import FastAPI

from routes.events import router as events_router
from routes.auth import router as auth_router
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exceptions.exceptions import InvalidLoginException


app = FastAPI(title='nc_plus_one_api')


app.include_router(events_router)
app.include_router(auth_router)




@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(InvalidLoginException)
def handle_invalid_login_attempt(request: Request, exc: InvalidLoginException):
    return JSONResponse(status_code=exc.status_code,content={'error':exc.detail})