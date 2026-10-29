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
    return JSONResponse(status_code=exc.status_code, content={'error':'invalid request', 'detail':exc.detail})

@app.exception_handler(InvalidLoginException)
def handle_invalid_login_attempt(request: Request, exc: InvalidLoginException):
    return JSONResponse(status_code=exc.status_code,content={'error':'invalid login', 'detail':exc.detail})

@app.exception_handler(RequestValidationError)
def handle_request_valdation_error(request: Request, exc: RequestValidationError):
    error_locs = []
    for e in exc.errors(): error_locs.extend([l for l in e['loc']])
    if 'password' in error_locs or 'email' in error_locs:
        response = JSONResponse(status_code=400,content={'error':'incomplete credentials', 'detail':'email or password not supplied'})
    else:
        print(error_locs)
        response = JSONResponse(status_code=400,content={'error':'invalid request', 'detail':'missing credentials or information'})
    return response