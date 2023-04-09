import os

from loguru import logger

from circleblock.changer import FileChanger
from circleblock.watcher import FileWatcher

if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    logger.info(f'Starting InitFileCreator')
    logger.info(f'Project root::{project_root}')
    creator = FileWatcher(project_root)
    creator.changer = FileChanger(project_root)
    # creator.create_init_files()
    creator.watch_for_changes()
