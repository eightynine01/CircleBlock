<div style="display: flex; justify-content: center;">
  <img src="images/logo.png" alt="CircleBlock Logo">

</div>
<div style="display: flex; justify-content: center;">
    <h1>CircleBlock</h1>
</div>



CircleBlock은 Python 프로젝트를 더 잘 구성하고 관리하기 위해 자동으로 `__init__.py` 파일을 업데이트하고 생성해주는 Python 패키지입니다. 프로젝트 파일 시스템을 감시하고 변경 내용에 따라 `__init__.py` 파일을 업데이트합니다. 이 패키지는 원형을 형상화한 블록 다이어그램을 기반으로 설계되었지만, 모든 Python 프로젝트에서 사용할 수 있습니다.

[Read in English](./README.md)

## 기능

- 프로젝트에 파일을 추가하거나 수정할 때 자동으로 `__init__.py` 파일 업데이트
- 프로젝트 루트 디렉토리의 파일 시스템 감시
- 영어와 한국어 모두 지원
- 디버깅 및 모니터링을 위한 자세한 로깅
- Python 프로젝트와 쉽게 통합 가능

## 설치

pip를 사용하여 CircleBlock을 설치할 수 있습니다:

```
pip install circleblock
```

## 사용 방법

`ccbk` 명령어를 사용하여 `start` 하위 명령어를 실행하여 CircleBlock을 시작할 수 있습니다:

```
ccbk start
```

기본적으로 CircleBlock은 현재 작업 디렉토리를 감시합니다. 다른 프로젝트 루트 디렉토리를 지정하려면 `--project-root` 또는 `-p` 옵션을 사용하세요:

```
ccbk start --project-root /path/to/your/project
```

로그 레벨을 설정하려면 `--log-level` 또는 `-l` 옵션을 사용하세요:

```
ccbk start --log-level DEBUG
```

프로젝트의 모든 `__init__.py` 파일을 초기화하고 업데이트하려면 `--init` 또는 `-i` 플래그를 사용하세요:

```
ccbk start --init
```

사용 가능한 옵션에 대한 자세한 내용은 다음 명령을 실행하세요:

```
ccbk --help
```

## 기여

기여를 환영합니다! 기능 요청, 버그 보고 또는 CircleBlock을 개선하기 위한 다른 아이디어가 있다면 프로젝트의 GitHub 저장소에서 이슈를 열어주세요. 당신의 의견과 지원에 감사드립니다.

## 라이선스

CircleBlock은 MIT 라이선스로 출시됩니다.