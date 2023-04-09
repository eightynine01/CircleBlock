import os
import sys
from typing import Optional

from loguru import logger

from changer import InitFileUpdater
from watcher import FileWatcher


class CircleBlock:
    """
    CircleBlock은 프로젝트 루트 디렉토리 내의 파일 시스템을 감시하는 클래스입니다.
    CircleBlock is a class that monitors the file system in the project root directory.
    """

    def __init__(self, project_root: str):
        """
        CircleBlock 객체를 생성합니다.
        Create a CircleBlock object.

        :param project_root: 프로젝트 루트 디렉토리 경로 (Project root directory path)
        """
        self.project_root = project_root
        self.updater = InitFileUpdater(project_root)
        self.watcher = FileWatcher(project_root, self.updater)

    def start_watching(self):
        """
        파일 시스템 감시를 시작합니다.
        Start monitoring the file system.
        """
        self.watcher.start_watching()
        logger.info(f'{self.project_root}의 파일 시스템 감시를 시작합니다. Start monitoring the file system in {self.project_root}.')

    def stop_watching(self):
        """
        파일 시스템 감시를 종료합니다.
        Stop monitoring the file system.
        """
        self.watcher.stop_watching()
        logger.info(f'{self.project_root}의 파일 시스템 감시를 종료합니다. Stop monitoring the file system in {self.project_root}.')


def start_circleblock(project_root: str, log_level: Optional[str] = 'INFO'):
    """
    CircleBlock을 시작합니다.
    Start CircleBlock.

    :param project_root: 프로젝트 루트 디렉토리 경로 (Project root directory path)
    :param log_level: 로그 레벨 (default: 'INFO') (Log level (default: 'INFO'))
    """
    logger.remove()
    logger.add(
        sink=sys.stderr if log_level == 'DEBUG' else sys.stdout,
        level=log_level,
        format='{time} - {name} - {level} - {message}'
    )
    circleblock = CircleBlock(project_root)
    circleblock.start_watching()


if __name__ == '__main__':
    """
    프로젝트 루트 디렉토리를 설정하고, CircleBlock을 시작합니다.
    Set the project root directory and start CircleBlock.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    logger.info('CircleBlock 시작합니다. Start CircleBlock.')
    logger.info(f'프로젝트 루트 디렉토리 경로: {project_root} Project root directory path: {project_root}')
    start_circleblock(project_root)
