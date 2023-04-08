import importlib
import os
from importlib import machinery

from loguru import logger

def process_all_files(package_path):
    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                functions, classes = get_functions_and_classes(file_path)
                for func_name, line_number in functions + classes:
                    logger.info(f"{file_path}:{line_number}: {func_name}")
                    logger.info(get_import_line(file_path, func_name))


def get_functions_and_classes(file_path):
    functions = []
    classes = []

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if 'def ' in line:
                line = line.strip()
                func_name = line.split('def ')[1].split('(')[0]
                functions.append((func_name, i + 1))
            elif 'async def ' in line:
                line = line.strip()
                func_name = line.split('async def ')[1].split('(')[0]
                functions.append((func_name, i + 1))
            elif 'class ' in line:
                line = line.strip()
                class_name = line.split('class ')[1].split(':')[0]
                classes.append((class_name, i + 1))

    return functions, classes


def get_module_files(module_path):
    files = []

    for dirpath, dirnames, filenames in os.walk(module_path):
        for filename in filenames:
            if filename.endswith('.py'):
                files.append(os.path.join(dirpath, filename))

    return files


def import_file(file_path):
    module_name = os.path.basename(file_path).replace('.py', '')
    loader = importlib.machinery.SourceFileLoader(module_name, file_path)
    module = loader.load_module()

    return module


def get_import_line(file_path, func_or_class_name):
    module_name = os.path.basename(file_path).replace('.py', '')
    module = import_file(file_path)

    if hasattr(module, func_or_class_name):
        return f"from .{module_name} import {func_or_class_name}"
    else:
        return f"from .{module_name} import {func_or_class_name} as {module_name}_{func_or_class_name}"


def process_files(module_path):
    files = get_module_files(module_path)

    for file_path in files:
        functions, classes = get_functions_and_classes(file_path)
        for func_name, line_number in functions + classes:
            logger.info(f"{file_path}:{line_number}: {func_name}")
            logger.info(get_import_line(file_path, func_name))
