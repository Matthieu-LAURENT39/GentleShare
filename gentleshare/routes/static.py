from . import main
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import (
    ObjectDoesNotExistError,
)
from sqlalchemy_file.storage import StorageManager
from flask import abort, send_file, current_app
from loguru import logger
from os import getcwd
from os.path import join


# Code from https://github.com/jowilf/sqlalchemy-file/blob/main/examples/flask/app.py
@main.route("/medias/<storage>/<file_id>")
def serve_files(storage, file_id):
    """Route to serve files from the storage"""
    logger.debug(f"Requested file {file_id} from storage {storage}")
    try:
        file = StorageManager.get_file(f"{storage}/{file_id}")
        if isinstance(file.object.driver, LocalStorageDriver):
            logger.debug(
                f"File {file_id} is stored in local storage ({file.get_cdn_url()}"
            )
            # If file is stored in local storage, just return a
            # FileResponse with the fill full path
            return send_file(
                join(getcwd(), file.get_cdn_url()),
                mimetype=file.content_type,
                download_name=file.filename,
            )
        elif file.get_cdn_url() is not None:
            # If file has public url, redirect to this url
            return current_app.redirect(file.get_cdn_url())
        else:
            # Otherwise, return a streaming response
            return current_app.response_class(
                file.object.as_stream(),
                mimetype=file.content_type,
                headers={"Content-Disposition": f"attachment;filename={file.filename}"},
            )
    except ObjectDoesNotExistError:
        abort(404)
