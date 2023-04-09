# CircleBlock 삭제
pipenv uninstall CircleBlock

# 빌드된 파일 삭제
rm -rf CircleBlock.egg-info/ build/ dist

# 배포용 파일 생성
pipenv install .