from sqlalchemy_file.storage import StorageManager
from libcloud.storage.drivers.local import LocalStorageDriver
from tempfile import TemporaryDirectory
from flask import Flask, current_app
import atexit
from contextlib import suppress, nullcontext

import os
from os.path import join


def setup_storage_manager(
    app: Flask | None = None, ignore_if_already_registered: bool = False
) -> StorageManager:
    """
    Gets the current storage manager for the app
    If no app is provided, the current app will be used
    """

    if app is None:
        app = current_app

    if app.config["TESTING"]:
        tmp_dir = TemporaryDirectory(prefix="gentleshare_test_file_storage")
        # Delete the temporary directory on program exit
        atexit.register(tmp_dir.cleanup)

        # Configure Storage
        os.makedirs(join(tmp_dir.name, "files"), 0o700, exist_ok=True)
        files_container = LocalStorageDriver(tmp_dir.name).get_container("files")

    else:
        # Configure Storage
        os.makedirs("./uploads/files", 0o700, exist_ok=True)
        files_container = LocalStorageDriver("./uploads").get_container("files")

    with suppress(RuntimeError) if ignore_if_already_registered else nullcontext():
        StorageManager.add_storage("files", files_container)
