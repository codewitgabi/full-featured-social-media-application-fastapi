import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

load_dotenv()

# custom imports

from api.v1.responses.error_responses import ValidationErrorResponse


app: FastAPI = FastAPI(
    debug=os.environ.get("DEBUG") != "False",
    docs_url=None,
    redoc_url=None,
    title="Fastapi Social Media API",
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


@app.get("/")
async def index():
    return {
        "status": status.HTTP_200_OK,
        "message": "Welcome to fastapi-social-media-api",
        "data": {},
    }


# start server

if __name__ == "__main__":
    uvicorn.run(app, port=int(os.environ.get("SERVER_PORT", 5001)), reload=False)
