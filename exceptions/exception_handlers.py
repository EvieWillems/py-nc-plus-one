from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from main import app


# @app.exception_handler(HTTPException)
# def handle_http_exception(request: Request, exc: HTTPException):
#     return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

# @app.exception_handler(RequestValidationError)
# def handle_request_validation(request: Request, exc: RequestValidationError):
