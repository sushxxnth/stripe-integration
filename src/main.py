from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.middleware.sessions import SessionMiddleware


from src.core.models import Response, ResponseCode
from src.router.endpoints import api_router
from src.core import settings


app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.get("/")
def get_docs():
    return RedirectResponse("/docs")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = []
    for error in errors:
        custom_errors.append({"field": error["loc"][-1], "message": error["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=Response(
            success=False, response_code=ResponseCode.bad_request, data=custom_errors
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exec: HTTPException):
    return JSONResponse(
        status_code=exec.status_code,
        content=Response(
            success=False, response_code=ResponseCode.bad_request, message=exec.detail
        ).model_dump(),
    )


app.include_router(api_router, prefix="/api")
