import enum
import os
import signal
import sys

import typer

from daemonize import Daemonize

from .changer import InitFileUpdater
from .watcher import FileWatcher

app = typer.Typer(add_completion=True, help='CircleBlock CLI')


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
        typer.echo(f'Start monitoring the file system in {self.project_root}. {self.project_root}의 파일 시스템 감시를 시작합니다.')

    def stop_file_system_watch(self):
        """
        Stop monitoring the file system.
        파일 시스템 감시를 종료합니다.
        """
        self.watcher.stop_watching()
        typer.echo(f'Stop monitoring the file system in {self.project_root}. {self.project_root}의 파일 시스템 감시를 종료합니다.')


class CommandType(enum.IntEnum):
    RUN = enum.auto()
    STOP = enum.auto()
    INIT = enum.auto()


@app.callback()
def callback(
        ctx: typer.Context,
        project_root: str = typer.Option(None, '-p', '--project-root', help='Project root directory path')
):
    ctx.obj = {'project_root': project_root or os.getcwd(), 'cb': None}


@app.command(help='Start CircleBlock in daemon mode')
def run(ctx: typer.Context) -> None:
    cb: CircleBlock = ctx.obj['cb'] or CircleBlock(ctx.obj['project_root'])
    typer.echo(f'project_root::{ctx.obj["project_root"]}')

    def start():
        cb.watch_file_system()

    typer.echo(f'Starting CircleBlock in daemon mode')
    daemon = Daemonize(
        app='CircleBlock',
        pid=os.path.join(cb.project_root, 'CircleBlock.pid'),
        action=start
    )
    daemon.start()


@app.command(help='Stop CircleBlock daemon')
def stop(ctx: typer.Context) -> None:
    cb: CircleBlock = ctx.obj['cb'] or CircleBlock(ctx.obj['project_root'])

    pid_file = os.path.join(cb.project_root, 'CircleBlock.pid')
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        os.remove(pid_file)
        typer.echo(f'CircleBlock daemon with PID {pid} has been terminated.')
    else:
        typer.echo('CircleBlock daemon is not running or PID file is missing.')


@app.command(help='Initialize CircleBlock')
def init(ctx: typer.Context) -> None:
    cb: CircleBlock = ctx.obj['cb'] or CircleBlock(ctx.obj['project_root'])
    cb.updater.initialize_all_init_files()


if __name__ == '__main__':
    app(prog_name='circleblock', help_option_names=['--help'])

