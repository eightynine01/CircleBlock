import os
import importlib.machinery
import inspect
from typing import Tuple, List

import typer
from watchdog.events import FileSystemEvent, FileSystemEventHandler


def _is_external(module, obj) -> bool:
    """
    Check if the object is imported from an external module.

    외부 모듈에서 가져온 객체인지 확인.
    """
    module_of_obj = inspect.getmodule(obj)
    if module_of_obj is None:
        return False
    module_of_obj_name = getattr(module_of_obj, '__name__', None)
    if module_of_obj_name is None:
        return False
    package_name = module.__name__.rsplit('.', 1)[0]
    return not module_of_obj_name.startswith(package_name)


def _is_exportable(obj) -> bool:
    """
    Check if the object is exportable (function or class).

    객체가 내보낼 수 있는지 (함수 또는 클래스) 확인.
    """
    return (inspect.isfunction(obj) or inspect.isclass(obj)) and inspect.getmodule(obj) != obj.__class__


def _get_exports(module_path: str) -> Tuple[str, list[str]]:
    """
    Get a list of exportable functions within a module.

    모듈 내 내보낼 수 있는 함수 목록을 가져옴.
    """
    try:
        module_name = os.path.basename(module_path).replace('.py', '')
        loader = importlib.machinery.SourceFileLoader(module_name, module_path)
        module = loader.load_module()

        exports = [
            attr for attr in dir(module)
            if all([
                not attr.startswith('_'),
                not _is_external(module, getattr(module, attr)),
                _is_exportable(getattr(module, attr))
            ])
        ]
    except Exception as e:
        typer.echo(f'Error while importing {module_path}: {e}')
        return '', []
    return module_name, exports


def _get_exports_str(module_name: str, exports: List[str], imports: list) -> None:
    if not exports:
        return
    exports = ',\n'.join([f'    {export} as {module_name}_{export}' for export in exports])
    line_templates = f'from .{module_name} import (\n{exports}\n)\n'
    imports.append(line_templates)


def _write_imports_to_init_file(dirname, imports: List[str]) -> None:
    """
    Write importable functions to the circleblock_cli.py file in the given directory.

    주어진 디렉토리의 circleblock_cli.py 파일에 가져올 함수들을 작성.
    """
    if not imports:
        return
    with open(os.path.join(dirname, '__init__.py'), 'w', encoding='UTF8') as f:
        f.writelines(imports)


class InitFileUpdater(FileSystemEventHandler):
    def __init__(self, project_root: str):
        self.project_root = project_root

    def dispatch(self, event: FileSystemEvent):
        dirname = os.path.dirname(event.src_path)
        imports = self._collect_imports(dirname, event)
        _write_imports_to_init_file(dirname, imports)

    def _collect_imports(self, dirname: str, event: FileSystemEvent) -> list[str]:
        """
        Collect exportable functions from modules in a given directory.

        주어진 디렉토리의 모듈에서 내보낼 수 있는 함수를 모아 반환.
        """
        imports = []
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            if self._is_valid_event(event, dirname, filename):
                module_name, exports = _get_exports(filepath)
                _get_exports_str(module_name, exports, imports)
        return imports

    def _is_valid_event(self, event: FileSystemEvent, dirname: str, filename: str) -> bool:
        """
        Check if the event is valid.

        유효한 이벤트인지 확인.
        """
        sl = ['.', '_']
        return all([
            not event.is_directory,
            not any([*[filename.startswith(i) for i in sl], not filename.endswith('.py')]),
            dirname != os.path.dirname(os.path.abspath(__file__)),
            dirname != self.project_root,
        ])

    def initialize_all_init_files(self):
        """
        Find all the directories and create '__init__.py' files in each directory.
        Also write the import statements for all exportable functions in each package's `__init__.py` file.

        모든 디렉토리를 찾아서 각 디렉토리에 '__init__.py' 파일을 생성합니다.
        또한, 각 패키지의 `__init__.py` 파일에 있는 내보낼 수 있는 함수를 import 하는 코드를 작성합니다.
        """
        for root, dirs, files in os.walk(self.project_root):
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                imports = self._collect_imports(dir_path, FileSystemEvent(dir_path))
                _write_imports_to_init_file(dir_path, imports)
