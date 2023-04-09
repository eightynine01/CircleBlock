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
    msg_left = '[<level>{level}|</level><green>{time:YYYY-MM-DD HH:mm:ss}</green>]'
    msg_center = '[<cyan>{name}</cyan>:<cyan>{function}</cyan>:<red>{line}</red>]'
    msg_right = '<level>{message}</level>'
    default_msg_fmt = f'{msg_left}{msg_center} {msg_right}'
    logger.remove()
    logger.add(
        sink=sys.stderr if log_level == 'DEBUG' else sys.stdout,
        level=log_level,
        format=default_msg_fmt
    )
    circleblock = CircleBlock(project_root)
    logger.info('CircleBlock 시작합니다. Start CircleBlock.')
    logger.info(f'프로젝트 루트 디렉토리 경로: {project_root} Project root directory path: {project_root}')
    circleblock.start_watching()
