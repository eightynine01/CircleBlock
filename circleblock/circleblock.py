import enum
import os
import signal
import sys

import click
from daemonize import Daemonize
from loguru import logger

from .changer import InitFileUpdater
from .watcher import FileWatcher


class CircleBlock:
    '''
    CircleBlock is a class that monitors the file system in the project root directory.
    CircleBlock은 프로젝트 루트 디렉토리 내의 파일 시스템을 감시하는 클래스입니다.
    '''

    def __init__(self, project_root: str, init: bool = False):
        self.project_root = project_root
        self.updater = InitFileUpdater(project_root)
        self.watcher = FileWatcher(project_root, self.updater)
        if not init:
            return
        self.updater.initialize_all_init_files()

    def watch_file_system(self):
        '''
        Start monitoring the file system.
        파일 시스템 감시를 시작합니다.
        '''
        self.watcher.start_watching()
        logger.info(f'Start monitoring the file system in {self.project_root}. {self.project_root}의 파일 시스템 감시를 시작합니다.')

    def stop_file_system_watch(self):
        '''
        Stop monitoring the file system.
        파일 시스템 감시를 종료합니다.
        '''
        self.watcher.stop_watching()
        logger.info(f'Stop monitoring the file system in {self.project_root}. {self.project_root}의 파일 시스템 감시를 종료합니다.')


class CommandType(enum.IntEnum):
    RUN = enum.auto()
    STOP = enum.auto()
    INIT = enum.auto()


@click.group()
@click.option(
    '--project-root',
    '-p',
    default=os.getcwd(),
    help='Project root directory path (default: current directory) | 프로젝트 루트 디렉토리 경로 (기본값: 현재 디렉토리)'
)
@click.pass_context
def cli(ctx, project_root):
    ctx.ensure_object(dict)
    ctx.obj['project_root'] = project_root
    ctx.obj['cb'] = CircleBlock(project_root)


@click.command()
@click.pass_context
def run(ctx):
    cb: CircleBlock = ctx.obj['cb']

    def start():
        cb.watch_file_system()

    logger.info(f'Starting CircleBlock in daemon mode')
    daemon = Daemonize(
        app='CircleBlock',
        pid=os.path.join(ctx.obj['project_root'], 'CircleBlock.pid'),
        action=start
    )
    daemon.start()


@click.command()
@click.pass_context
def stop(ctx):
    cb: CircleBlock = ctx.obj['cb']
    cb.stop_file_system_watch()

    pid_file = os.path.join(ctx.obj['project_root'], 'CircleBlock.pid')
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        os.remove(pid_file)
        logger.info(f'CircleBlock daemon with PID {pid} has been terminated.')
    else:
        logger.warning('CircleBlock daemon is not running or PID file is missing.')


@click.command()
@click.pass_context
def init(ctx):
    cb: CircleBlock = ctx.obj['cb']
    cb.updater.initialize_all_init_files()


cli.add_command(run)
cli.add_command(stop)
cli.add_command(init)


if __name__ == '__main__':
    cli(prog_name='ccbk')

