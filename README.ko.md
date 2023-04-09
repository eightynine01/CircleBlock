<div style="display: flex; justify-content: center;">
  <img src="images/logo.png" alt="CircleBlock Logo">

</div>
<div style="display: flex; justify-content: center;">
    <h1>CircleBlock</h1>
</div>



CircleBlock은 프로젝트의 파일 시스템을 모니터링하여 모듈 내에서 내보낼 수 있는 함수들을 자동으로 `__init__.py` 파일에 추가하는 도구입니다. 이를 통해 패키지의 함수를 쉽게 가져올 수 있습니다.

[Read in English](./README.md)

## 설치

CircleBlock을 설치하려면 다음 명령어를 사용하세요:

```bash
pip install circleblock
```

## 사용법

CLI로 CircleBlock을 사용하려면 다음 명령어를 사용하세요:

```bash
ccbk run
```

다음 옵션들이 제공됩니다:

- `--project-root (-p)`: 프로젝트 루트 디렉토리 경로 (기본값: 현재 디렉토리)
- `--log-level (-l)`: 로그 레벨 (기본값: INFO)
- `--init (-i)`: 프로젝트 내 모든 `__init__.py` 파일을 초기화 및 업데이트 (기본값: False)

## 예제

다음과 같은 프로젝트 구조를 가정해봅시다:

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

`my_project` 디렉토리에서 `ccbk run` 명령어를 실행하면 CircleBlock이 파일 시스템을 모니터링하기 시작합니다. 모듈의 내용이 변경되면 CircleBlock은 자동으로 `__init__.py` 파일에 내보낼 수 있는 함수들을 업데이트합니다.

예를 들어, `module1.py`의 내용이 다음과 같다고 가정합니다:

```
def func_a():
    pass

def func_b():
    pass
```

이 경우, `package1` 디렉토리의 `__init__.py` 파일은 다음과 같이 업데이트됩니다:

```
from .module1 import (
    func_a,
    func_b,
)
```

이렇게 하면 패키지 자체에서 이러한 함수를 쉽게 가져올 수 있습니다:

```
from package1 import func_a, func_b
```

파일 시스템 모니터링을 중지하려면 `ccbk stop` 명령어를 사용하세요. 파일 시스템 모니터링을 시작하지 않고 프로젝트의 모든 `__init__.py` 파일을 초기화하고 업데이트하려면 `ccbk --init` 명령어를 사용하세요.