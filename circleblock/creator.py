import atexit
import importlib
import inspect
import os
import signal

from loguru import logger
from watchdog.observers import Observer

from utils import unused


class FileCreator:
    def __init__(self, root_dir: str, changer=None):
        self.root_dir = root_dir
        self.observer = Observer()
        self.changer = changer
        atexit.register(self.log_exit)

    def create_init_py(self, package_dir: str) -> None:
        """
        Create __init__.py file for the package with the list of __all__.

        Args:
            package_dir (str): The path to the package directory.
        """
        import_lines = []
        if package_dir == os.path.dirname(os.path.abspath(__file__)):
            return
        for filename in os.listdir(package_dir):
            name, ext = os.path.splitext(filename)
            if ext == '.py':
                module_name = f'{os.path.basename(package_dir)}.{name}'

                try:
                    module = importlib.import_module(module_name)

                    for _, obj in inspect.getmembers(module):
                        if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == module_name:
                            import_lines.append(f'from .{name} import {obj.__name__}')

                    logger.info(f'{package_dir} - {module_name} created')

                except (ImportError, AttributeError) as error:
                    logger.error(f'Error importing {module_name}: {error}')

        with open(os.path.join(package_dir, '__init__.py'), 'w') as f:
            f.write('\n'.join(import_lines) + '\n')

    def create_init_files(self) -> None:
        """
        Create __init__.py files for all packages under the root directory.
        """

        for dirpath, dirs, _ in os.walk(self.root_dir):
            if unused(os.path.basename(dirpath)):
                dirs.clear()
                continue
            if dirpath != self.root_dir:
                self.create_init_py(dirpath)

    def watch_for_changes(self):
        """
        Watch the root directory for changes and create/update __init__.py files accordingly.
        """

        self.observer.schedule(self.changer, self.root_dir, recursive=True)
        self.observer.start()
        signal.signal(signal.SIGINT, lambda: self.stop_watching)
        signal.pause()

    def stop_watching(self, *args, **kwargs):
        """
        Stop watching the root directory for changes.
        """
        self.observer.stop()
        self.observer.join()

    def log_exit(self):
        """
        Log exit message when the program exits.
        """
        logger.info('InitFileCreator stopped watching for changes.')
