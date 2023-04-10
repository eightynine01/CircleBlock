#!/usr/bin/env fish

# CircleBlock 배포 스크립트

# CircleBlock 삭제
pipenv uninstall CircleBlock

# 빌드된 파일 삭제
rm -rf CircleBlock.egg-info/ build/ dist

# 배포용 파일 생성
pipenv run python setup.py sdist bdist_wheel

# PyPI에 업로드
pipenv run twine upload dist/*
