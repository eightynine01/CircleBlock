import importlib
import inspect
import os
from importlib import machinery

from loguru import logger
from watchdog.events import FileSystemEventHandler, FileSystemEvent


def _is_external_import(module, obj):
    """Check if an object is imported from an external module."""
    module_of_obj = inspect.getmodule(obj)
    if module_of_obj is None:
        return False
    module_of_obj_name = getattr(module_of_obj, '__name__', None)
    if module_of_obj_name is None:
        return False
    package_name = module.__name__.rsplit('.', 1)[0]
    return not module_of_obj_name.startswith(package_name)


def _is_exportable(obj):
    """Check if an object is exportable (a function or a class)."""
    return (inspect.isfunction(obj) or inspect.isclass(obj)) and inspect.getmodule(obj) != obj.__class__


def _get_module_exports(module_path) -> tuple[str, list[str]]:
    """Get a dictionary of exported functions in a module."""
    logger.debug(f'module_path::{module_path}')
    module_name = os.path.basename(module_path).replace('.py', '')
    logger.debug(f'module_name::{module_name}')
    loader = importlib.machinery.SourceFileLoader(module_name, module_path)
    module = loader.load_module()

    exports = [
        attr for attr in dir(module)
        if all([
            not attr.startswith('_'),
            not _is_external_import(module, getattr(module, attr)),
            _is_exportable(getattr(module, attr))
        ])
    ]
    return module_name, exports


class FileChanger(FileSystemEventHandler):
    def __init__(self, project_root):
        self.project_root = project_root

    def dispatch(self, event: FileSystemEvent):
        sl = ['.', '_']
        dirname = os.path.dirname(event.src_path)
        imports = []
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            if all([
                not event.is_directory,
                not any([
                    *[filename.startswith(i) for i in sl],
                    not event.src_path.endswith('.py')
                ]),
                dirname != self.project_root,
            ]):
                module_name, exports = _get_module_exports(filepath)
                if exports:
                    exports = f',\n'.join([f'    {export}' for export in exports])
                    line_templates = f'from .{module_name} import (\n{exports}\n)\n'
                    imports.append(line_templates)
        if imports:
            with open(os.path.join(dirname, '__init__.py'), 'w', encoding='UTF8') as f:
                f.writelines(imports)

    def on_modified(self, event: FileSystemEvent):
        # TODO 분리해서 작성필요
        pass

    def on_created(self, event: FileSystemEvent):
        # TODO 분리해서 작성필요
        pass

    def on_deleted(self, event: FileSystemEvent):
        # TODO 분리해서 작성필요
        pass

    def _init_reset(self):
        # TODO 분리해서 작성필요
        pass
