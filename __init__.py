import os
import click
from circleblock import start_circleblock


@click.command()
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
def start(project_root, log_level):
    start_circleblock(project_root, log_level)


if __name__ == '__main__':
    start()
