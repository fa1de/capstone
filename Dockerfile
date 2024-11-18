# Python 3.9 기반 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리를 /app으로 설정 (컨테이너 내에서 실행될 작업 디렉토리)
WORKDIR /app

# requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt /app/

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# myproject 폴더를 컨테이너의 /app/myproject로 복사
COPY myproject /app/myproject

# 포트 8000을 외부에 노출
EXPOSE 8000

# Django 개발 서버 실행
CMD ["python", "myproject/manage.py", "runserver", "0.0.0.0:8000"]
