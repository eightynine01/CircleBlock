import os
import sys
from typing import Optional

import click
from daemonize import Daemonize
from loguru import logger

from .changer import InitFileUpdater
from .watcher import FileWatcher


class CircleBlock:
    """
    CircleBlock은 프로젝트 루트 디렉토리 내의 파일 시스템을 감시하는 클래스입니다.
    CircleBlock is a class that monitors the file system in the project root directory.
    """

    def __init__(self, project_root: str, init: bool = False):
        """
        CircleBlock 객체를 생성합니다.
        Create a CircleBlock object.

        :param project_root: 프로젝트 루트 디렉토리 경로 (Project root directory path)
        """
        self.project_root = project_root
        self.updater = InitFileUpdater(project_root)
        self.watcher = FileWatcher(project_root, self.updater)
        if not init:
            return
        self.updater.initialize_all_init_files()

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


def start_circleblock(project_root: str, log_level: Optional[str] = 'INFO', init: bool = False):
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


@click.group(name='ccbk')
@click.option(
    '--project-root',
    '-p',
    default=os.getcwd(),
    help='Project root directory path (default: current directory) | 프로젝트 루트 디렉토리 경로 (default: 실행위치)'
)
@click.option(
    '--log-level',
    '-l',
    default='INFO',
    help='Log level (default: INFO) | 로그 레벨 (default: INFO)'
)
@click.option(
    '--init',
    '-i',
    is_flag=True,
    default=False,
    help='Initialize and update all __init__.py files in the project | 프로젝트 내 모든 __init__.py 파일을 초기화 및 업데이트'
)
@click.pass_context
def cli(ctx, project_root, log_level, init):
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
    ctx.obj = CircleBlock(project_root, init)


@click.command()
@click.pass_obj
def run(cb: CircleBlock, daemon: bool = True):
    if daemon:
        def start():
            cb.start_watching()

        logger.info(f"Starting CircleBlock in daemon mode")
        daemon = Daemonize(
            app="CircleBlock",
            pid=os.path.join(cb.project_root, "CircleBlock.pid"),
            action=start
        )
        daemon.start()
    else:
        cb.start_watching()


@click.command()
@click.pass_obj
def stop(cb: CircleBlock):
    cb.stop_watching()
