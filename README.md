<div style="display: flex; justify-content: center;">
  <img src="images/logo.png" alt="CircleBlock Logo">

</div>
<div style="display: flex; justify-content: center;">
    <h1>CircleBlock</h1>
</div>

CircleBlock is a Python package that automatically updates and generates `__init__.py` files for better organization and management of your Python projects. It monitors your project's file system and updates the `__init__.py` files accordingly as you make changes. The package is designed to work with circular-themed block diagrams, but it can be used in any Python project.

[한국어로 읽기](./README.ko.md)

## Features

- Automatic update of `__init__.py` files as you add or modify files in your project
- Monitors the file system of the project root directory
- Support for both English and Korean languages
- Detailed logging for easy debugging and monitoring
- Easy installation and integration with your Python project

## Installation

You can install CircleBlock using pip:

```
pip install circleblock
```

## Usage

You can start CircleBlock by running the `ccbk` command with the `start` subcommand:

```
ccbk start
```

By default, CircleBlock will start monitoring the current working directory. You can specify a different project root directory using the `--project-root` or `-p` option:

```
ccbk start --project-root /path/to/your/project
```

To set the log level, use the `--log-level` or `-l` option:

```
ccbk start --log-level DEBUG
```

To initialize and update all `__init__.py` files in your project, use the `--init` or `-i` flag:

```
ccbk start --init
```

For more information about the available options, run:

```
ccbk --help
```

## Contributing

Contributions are welcome! If you have a feature request, bug report, or any other ideas to improve CircleBlock, please open an issue on the project's GitHub repository. We appreciate your feedback and support.

## License

CircleBlock is released under the MIT License.