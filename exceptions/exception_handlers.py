# from fastapi import HTTPException, Request
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from main import app
# from exceptions import InvalidLoginException



# @app.exception_handler(HTTPException)
# def handle_http_exception(request: Request, exc: HTTPException):
#     return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

# @app.exception_handler(InvalidLoginException)
# def handle_invalid_login_attempt(request: Request, exc: InvalidLoginException):
#     return JSONResponse(status_code=exc.status_code,content={'error':exc.detail})
