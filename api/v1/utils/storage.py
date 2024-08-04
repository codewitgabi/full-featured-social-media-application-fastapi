from dotenv import load_dotenv
import os

load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api

config = cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload(file):
    """File upload handler

    :usage: res = upload(request_file.file.read())
    """

    response = cloudinary.uploader.upload(
        file,
        unique_filename=False,
        overwrite=True,
        asset_folder="chat-stream-api",
        resource_type="auto",
    )

    return response.get("secure_url")
