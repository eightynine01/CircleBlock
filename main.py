from loguru import logger

from circleblock import FileCreator, FileChanger

if __name__ == '__main__':
    logger.info('Starting InitFileCreator')
    creator = FileCreator('.')
    creator.changer = FileChanger(creator)
    creator.create_init_files()
    creator.watch_for_changes()
