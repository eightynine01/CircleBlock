<div style="display: flex; justify-content: center;">
  <img src="images/logo.png" alt="CircleBlock Logo">

</div>
<div style="display: flex; justify-content: center;">
    <h1>CircleBlock</h1>

</div>

CircleBlock is a class that monitors the file system in the project root directory. This class detects changes in the file system and automatically updates the exportable functions of each module in each package's `__init__.py` file.

[![English](https://img.shields.io/badge/language-English-orange.svg)](README.md) [![Korean](https://img.shields.io/badge/language-Korean-blue.svg)](README.ko.md)

## Features

1. Start/stop file system monitoring
2. Get a list of exportable functions within a module
3. Initialize and update all `__init__.py` files in a directory

## Installation

To install CircleBlock, use the following command:

```
pipenv install circleblock
```

## Usage (CLI)

### Start monitoring

To start monitoring the file system, use the following command:

```
ccbk run
```

### Stop monitoring

To stop monitoring the file system, use the following command:

```
ccbk stop
```

### Initialize and update `__init__.py` files

To initialize and update all `__init__.py` files in the project, use the following command:

```
ccbk --init
```

## Options

The options available for the `ccbk` command are as follows:

- `--project-root (-p)`: Project root directory path (default: current directory)
`--log-level (-l)`: Log level (default: INFO)
- `--init (-i)`: Initialize and update all `__init__.py` files in the project (default: False)

## _Example_

Assume you have a project structure like this:

```
my_project/
    ├── package1/
    │   ├── module1.py
    │   ├── module2.py
    │   └── __init__.py
    └── package2/
        ├── module3.py
        ├── module4.py
        └── __init__.py
```

If you run `ccbk run` in the `my_project` directory, CircleBlock will start monitoring the file system. Whenever there's a change in any of the modules, CircleBlock will automatically update the `__init__.py` files with the exportable functions.

For instance, if `module1.py` has the following content:

```
def func_a():
    pass

def func_b():
    pass
```

The `__init__.py` file in the `package1` directory will be updated with the following content:

```
from .module1 import (
    func_a,
    func_b,
)
```

This way, you can easily import these functions from the package itself:

```
from package1 import func_a, func_b
```

If you want to stop the file system monitoring, simply run the `ccbk stop` command. To initialize and update all `__init__.py` files in the project without starting the file system monitoring, use the `ccbk --init` command.