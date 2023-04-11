import os
import signal
import sys

import daemonocle
import typer

from circleblock.changer import InitFileUpdater
from circleblock.watcher import FileWatcher

sys.path.append(os.getcwd())

app = typer.Typer(add_completion=True, help='CircleBlock CLI')


class CircleBlock:
    """
    CircleBlock is a class that monitors the file system in the project root directory.
    CircleBlock은 프로젝트 루트 디렉토리 내의 파일 시스템을 감시하는 클래스입니다.
    """

    def __init__(self, _project_path: str = os.getcwd(), _init: bool = False):
        self.project_path = _project_path
        self.updater = InitFileUpdater(_project_path)
        self.watcher = FileWatcher(_project_path, self.updater)
        if _init:
            self.updater.initialize_all_init_files()

    def start(self):
        """
        Start monitoring the file system.
        파일 시스템 감시를 시작합니다.
        """
        pidfile_path = self.get_pid_file_path(self.project_path)

        if os.path.exists(pidfile_path):
            typer.echo("CircleBlock 데몬이 이미 실행 중입니다.")
            return

        daemon = daemonocle.Daemon(
            workdir=self.project_path,
            pidfile=pidfile_path,
            worker=self._run_watcher
        )
        daemon.do_action('start')

    def _run_watcher(self):
        try:
            self.watcher.start()
            typer.echo(f'CircleBlock 데몬(PID: {os.getpid()})이 시작되었습니다.')
            signal.pause()
        except Exception as e:
            typer.echo(f'Error: {e}')
            return

    def stop(self):
        """
        Stop monitoring the file system.
        파일 시스템 감시를 종료합니다.
        """
        pidfile_path = self.get_pid_file_path(self.project_path)

        if not os.path.exists(pidfile_path):
            typer.echo('CircleBlock 데몬이 실행 중이지 않습니다.')
            return

        with open(pidfile_path, 'r') as f:
            pid = int(f.read().strip())

        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            typer.echo(f'CircleBlock 데몬 프로세스(PID: {pid})을 찾을 수 없습니다. 이미 종료되었을 수 있습니다.')

        os.remove(pidfile_path)
        typer.echo(f'CircleBlock 데몬(PID: {pid})이 종료되었습니다.')

    @staticmethod
    def get_pid_file_path(project_path: str) -> str:
        return os.path.join(project_path, '_CircleBlock.pid')


def get_work_dir() -> str:
    return typer.Option(os.getcwd(), '-w', '--work_dir', help='프로젝트 루트 디렉토리 경로')


@app.command(help='CircleBlock 데몬 시작')
def run(work_dir: str = get_work_dir()) -> None:
    cb = CircleBlock(work_dir)
    cb.start()


@app.command(help='CircleBlock 데몬 종료')
def stop(work_dir: str = get_work_dir()) -> None:
    cb = CircleBlock(work_dir)
    cb.stop()


@app.command(help='CircleBlock 초기화')
def init(work_dir: str = get_work_dir()) -> None:
    CircleBlock(work_dir, _init=True)
    typer.echo(f'프로젝트 루트 디렉토리 {work_dir}에서 CircleBlock을 초기화했습니다.')


if __name__ == '__main__':
    app(help_option_names=['--help'])
