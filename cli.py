import enum
import os
import signal
from typing import Optional

import typer

from daemonize import Daemonize
from loguru import logger

from circleblock.changer import InitFileUpdater
from circleblock.watcher import FileWatcher

app = typer.Typer()


class CircleBlock:
    """
    CircleBlock is a class that monitors the file system in the project root directory.
    CircleBlock은 프로젝트 루트 디렉토리 내의 파일 시스템을 감시하는 클래스입니다.
    """

    def __init__(self, project_root: str, init: bool = False):
        self.project_root = project_root
        self.updater = InitFileUpdater(project_root)
        self.watcher = FileWatcher(project_root, self.updater)
        if not init:
            return
        self.updater.initialize_all_init_files()

    def watch_file_system(self):
        """
        Start monitoring the file system.
        파일 시스템 감시를 시작합니다.
        """
        self.watcher.start_watching()
        logger.info(f'Start monitoring the file system in {self.project_root}. {self.project_root}의 파일 시스템 감시를 시작합니다.')

    def stop_file_system_watch(self):
        """
        Stop monitoring the file system.
        파일 시스템 감시를 종료합니다.
        """
        self.watcher.stop_watching()
        logger.info(f'Stop monitoring the file system in {self.project_root}. {self.project_root}의 파일 시스템 감시를 종료합니다.')


class CommandType(enum.IntEnum):
    RUN = enum.auto()
    STOP = enum.auto()
    INIT = enum.auto()


@app.callback()
def callback(ctx: typer.Context):
    ctx.obj = {'project_root': os.getcwd(), 'cb': None}


@app.command()
def run(ctx: typer.Context) -> None:
    cb: CircleBlock = ctx.obj['cb'] or CircleBlock(ctx.obj['project_root'])

    def start():
        cb.watch_file_system()

    typer.echo(f'Starting CircleBlock in daemon mode')
    daemon = Daemonize(
        app='CircleBlock',
        pid=os.path.join(cb.project_root, 'CircleBlock.pid'),
        action=start
    )
    daemon.start()


@app.command()
def stop(ctx: typer.Context) -> None:
    cb: CircleBlock = ctx.obj['cb'] or CircleBlock(ctx.obj['project_root'])
    cb.stop_file_system_watch()

    pid_file = os.path.join(cb.project_root, 'CircleBlock.pid')
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        os.remove(pid_file)
        typer.echo(f'CircleBlock daemon with PID {pid} has been terminated.')
    else:
        typer.echo('CircleBlock daemon is not running or PID file is missing.')


@app.command()
def init(ctx: typer.Context) -> None:
    cb: CircleBlock = ctx.obj['cb'] or CircleBlock(ctx.obj['project_root'])
    cb.updater.initialize_all_init_files()


@app.command()
def ccbk(
        ctx: typer.Context,
        command: Optional[str],
        project_root: Optional[str] = typer.Argument(None, help='Project root directory path')
) -> None:
    if project_root:
        ctx.obj['project_root'] = project_root
    if ctx.obj['cb'] is None:
        ctx.obj['cb'] = CircleBlock(ctx.obj['project_root'])
    {
        CommandType.RUN: run,
        CommandType.STOP: stop,
        CommandType.INIT: init
    }[CommandType(command)](ctx)


if __name__ == '__main__':
    app()
