import signal

from loguru import logger
from watchdog.observers import Observer


class FileWatcher:
    def __init__(self, project_root: str, changer=None):
        self.project_root = project_root
        self.changer = changer
        self.observer = Observer()

    def start_watching(self):
        """
        변경 사항을 감시하기 위해 루트 디렉토리를 감시하고 circleblock_cli.py 파일을 생성/업데이트합니다.
        """
        logger.debug('변경 사항 감시 시작...')
        logger.debug(f'프로젝트 루트: {self.project_root}')

        self.observer.schedule(self.changer, self.project_root, recursive=True)
        self.observer.start()
        signal.signal(signal.SIGINT, lambda *args, **kwargs: self.stop_watching())
        signal.pause()

    def stop_watching(self):
        """
        변경 사항을 감지하는 루트 디렉토리의 감시를 중지합니다.
        """
        self.observer.stop()
        self.observer.join()
