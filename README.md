# CircleBlock

CircleBlock is a Python package that detects file creation, deletion, and modification events in a project directory, and updates the `__init__.py` file in that directory accordingly. This allows users to access all functions and classes within the project by simply importing the module, such as `import circleblock`, instead of specifying individual files.

This project uses [Python watchdog](https://pypi.org/project/watchdog/) to receive file system events, and [Loguru](https://github.com/Delgan/loguru) for logging.

## Usage

1. Install the `circleblock` package.
   ```
   pip install circleblock
   ```

2. Instantiate the `circleblock.FileWatcher` class with the path to the directory you want to monitor as an argument.
   ```python
   from circleblock.circleblock import FileWatcher

   watcher = FileWatcher(project_root='/path/to/project')
   ```

3. Call the `watcher.start_watching()` method to start monitoring files. This method starts an event loop, so it will enter an infinite loop. Pressing Ctrl-C will exit the program.
   ```
   watcher.start_watching()
   ```

4. To start CircleBlock via CLI, use the following command:
   ```
   circleblock start --project-root /path/to/project --log-level INFO
   ```

## Notes

- To import from this package, you need to configure the module to be importable in `__init__.py`.
- Subdirectories of the monitored directory can also be monitored.
- Currently, only file monitoring is supported, and directory monitoring is not supported.

## Development Environment
- Python 3.6 or higher
- Tested on macOS

## Contributing
If you would like to contribute to this project, please refer to the CONTRIBUTING.md file on GitHub.

## License
CircleBlock is licensed under the MIT License. See the LICENSE file for more information.

---

# CircleBlock

CircleBlock은 Python 프로젝트의 디렉토리에서 파일이 생성, 삭제, 수정되었을 때 이벤트를 감지하여 해당 디렉토리의 `__init__.py` 파일을 업데이트합니다. 이를 통해 프로젝트의 함수 또는 클래스를 import할 때 직접 파일을 지정하는 대신 `import circleblock`와 같이 모듈만 import하면 모든 함수 및 클래스에 접근할 수 있습니다. 

이 프로젝트는 [Python watchdog](https://pypi.org/project/watchdog/)를 사용하여 파일 시스템 이벤트를 수신하고, [Loguru](https://github.com/Delgan/loguru)를 사용하여 로깅하고 있습니다.

## 사용 방법

### Python Module로 사용하기

1. `circleblock` 모듈을 설치합니다.
```
pip install circleblock
```

2. 프로젝트 루트 디렉토리를 지정하여 `start_circleblock()` 함수를 호출합니다. 로그 레벨은 옵션으로 지정할 수 있습니다.

```python
from circleblock.circleblock import start_circleblock

project_root = '/path/to/project'
start_circleblock(project_root, log_level='INFO')
```

### CLI로 사용하기

1. `circleblock` 모듈을 설치합니다.
```
pip install circleblock
```

2. `circleblock start` 명령어를 실행합니다. `--project-root` 옵션으로 프로젝트 루트 디렉토리를, `--log-level` 옵션으로 로그 레벨을 지정할 수 있습니다. 
```sh
circleblock start --project-root /path/to/project --log-level INFO
```

## 참고사항

- 해당 모듈에서 import하려면 해당 모듈을 `__init__.py`에서 import할 수 있도록 설정해야 합니다.
- 감시 대상 디렉토리의 하위 디렉토리에 대해서도 감시가 가능합니다.
- 현재 파일 감시만 가능하며, 디렉토리 감시는 지원하지 않습니다.

## 개발 환경

- Python 3.6 이상
- macOS, Linux, Windows에서 테스트됨

## 기여하기

이 프로젝트에 기여하고 싶으신 분은 GitHub의 [CONTRIBUTING.md](./CONTRIBUTING.md) 파일을 참고해주세요.

## 라이선스

CircleBlock은 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참고해주세요.

