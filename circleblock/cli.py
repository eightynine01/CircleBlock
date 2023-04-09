import os
import click

from circleblock.circleblock import start_circleblock


@click.group(name='ccbk')
def cli():
    pass


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
@click.option(
    '--init',
    '-i',
    is_flag=True,
    default=False,
    help='Initialize and update all __init__.py files in the project | 프로젝트 내 모든 __init__.py 파일을 초기화 및 업데이트'
)
def start(project_root, log_level, init):
    start_circleblock(project_root, log_level, init)


if __name__ == '__main__':
    cli()
