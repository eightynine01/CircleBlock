import os
import importlib.machinery
import inspect
from watchdog.events import FileSystemEvent, FileSystemEventHandler


def is_external(module, obj) -> bool:
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


def is_exportable(obj) -> bool:
    """
    Check if the object is exportable (function or class).

    객체가 내보낼 수 있는지 (함수 또는 클래스) 확인.
    """
    return (inspect.isfunction(obj) or inspect.isclass(obj)) and inspect.getmodule(obj) != obj.__class__


def get_exports(module_path: str) -> tuple[str, list[str]]:
    """
    Get a list of exportable functions within a module.

    모듈 내 내보낼 수 있는 함수 목록을 가져옴.
    """
    module_name = os.path.basename(module_path).replace('.py', '')
    loader = importlib.machinery.SourceFileLoader(module_name, module_path)
    module = loader.load_module()

    exports = [
        attr for attr in dir(module)
        if all([
            not attr.startswith('_'),
            not is_external(module, getattr(module, attr)),
            is_exportable(getattr(module, attr))
        ])
    ]
    return module_name, exports


class InitFileUpdater(FileSystemEventHandler):
    def __init__(self, project_root: str):
        self.project_root = project_root

    def dispatch(self, event: FileSystemEvent):
        dirname = os.path.dirname(event.src_path)
        imports = self._collect_imports(dirname, event)

        if imports:
            self._write_imports_to_init_file(dirname, imports)

    def _collect_imports(self, dirname: str, event: FileSystemEvent) -> list[str]:
        """
        Collect exportable functions from modules in a given directory.

        주어진 디렉토리의 모듈에서 내보낼 수 있는 함수를 모아 반환.
        """
        sl = ['.', '_']
        imports = []
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            if self._is_valid_event(event, dirname, filename):
                module_name, exports = get_exports(filepath)
                if exports:
                    exports = ',\n'.join([f'    {export}' for export in exports])
                    line_templates = f'from .{module_name} import (\n{exports}\n)\n'
                    imports.append(line_templates)
        return imports

    def _is_valid_event(self, event: FileSystemEvent, dirname: str, filename: str) -> bool:
        """
        Check if the event is valid.

        유효한 이벤트인지 확인.
        """
        sl = ['.', '_']
        return all([
            not event.is_directory,
            not any([
                *[filename.startswith(i) for i in sl],
                not event.src_path.endswith('.py')
            ]),
            dirname != self.project_root,
        ])

    def _write_imports_to_init_file(self, dirname: str, imports: list[str]) -> None:
        """
        Write importable functions to the __init__.py file in the given directory.

        주어진 디렉토리의 __init__.py 파일에 가져올 함수들을 작성.
        """
        with open(os.path.join(dirname, 'circleblock/__init__.py'), 'w', encoding='UTF8') as f:
            f.writelines(imports)

    def on_modified(self, event: FileSystemEvent):
        # TODO: Separate and implement
        pass

    def on_created(self, event: FileSystemEvent):
        # TODO: Separate and implement
        pass

    def on_deleted(self, event: FileSystemEvent):
        # TODO: Separate and implement
        pass

    def _reset_init(self):
        # TODO: Separate and implement
        pass
