import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, FastAPIError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.exceptions import HTTPException as StarletteHttpException
from sqlalchemy.exc import InvalidRequestError

from api.v1.utils.database import Base, engine
from api.v1.routes import version_one

load_dotenv()

# custom imports

from api.v1.responses.error_responses import ValidationErrorResponse, ErrorResponse
from api.v1.responses.success_response import success_response


# create database tables

Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    debug=os.environ.get("DEBUG") != "False",
    docs_url="/docs",
    redoc_url=None,
    title="Fastapi Social Media API",
)

# routes

app.include_router(version_one)  # api version one

# cors handler

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# validation exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": error.get("loc")[-1],
                "message": error.get("msg"),
            }
        )
    response = ValidationErrorResponse(errors=errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response.model_dump()
    )


@app.exception_handler(StarletteHttpException)
async def http_exception_handler(request: Request, exc: StarletteHttpException):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())


@app.exception_handler(InvalidRequestError)
async def http_exception_handler(request: Request, exc: InvalidRequestError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=exc._message()
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump()
    )

@app.exception_handler(FastAPIError)
async def http_exception_handler(request: Request, exc: FastAPIError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=exc.detail
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump()
    )


@app.get("/")
async def index():
    return success_response(message="Welcome to fastapi-social-media-api")


# start server

if __name__ == "__main__":
    uvicorn.run(app, port=int(os.environ.get("SERVER_PORT", 5001)), reload=False)
