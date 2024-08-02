from typing import Optional
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    message: str, status_code: int = status.HTTP_200_OK, data: Optional[dict] = None
):
    """
    :param message: description of the response
    :param status_code: HTTP status code
    :param data: optional dictionary data

    :description: Renders a json response for uniformity accross all api endpoints.
    """

    response: dict = {
        "status_code": status_code,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))
