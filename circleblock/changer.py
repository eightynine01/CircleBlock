import os

from loguru import logger
from watchdog.events import FileSystemEventHandler

from utils import unused
from utils.maker import process_all_files


class FileChanger(FileSystemEventHandler):
    def __init__(self, _init_file_creator):
        self._init_file_creator = _init_file_creator

    def dispatch(self, event):
        file_name = os.path.basename(event.src_path)
        if all([
            not event.is_directory,
            event.src_path != self._init_file_creator.root_dir,
            not unused(file_name)
        ]):
            super().dispatch(event)

    def on_modified(self, event):
        self.create_init_py(event)

    def on_created(self, event):
        logger.info(event)
        logger.info('')

        self.create_init_py(event)

    def on_deleted(self, event):
        logger.info(event)
        logger.info('')

        self.create_init_py(event)

    def create_init_py(self, event) -> None:
        # file_name = os.path.basename(event.src_path)
        package_dir = os.path.dirname(event.src_path)
        process_all_files(package_dir)
        # self._init_file_creator.create_init_py(package_dir)

