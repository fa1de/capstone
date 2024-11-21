import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ROOT_URLCONF = "config.urls"

from django.core.management.utils import get_random_secret_key

SECRET_KEY = get_random_secret_key()

# 정적 파일을 위한 URL 설정
STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

X_FRAME_OPTIONS = "SAMEORIGIN"

# 템플릿 설정에 DjangoTemplates 추가
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # 템플릿 디렉토리 추가
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 미들웨어에 관련된 설정 추가
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # 세션 미들웨어 추가
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # 인증 미들웨어 추가
    "django.contrib.messages.middleware.MessageMiddleware",  # 메시지 미들웨어 추가
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 앱 추가 및 관리자 URL 설정
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "myapp",  # 여기에 설치한 앱을 추가합니다.
]

# 데이터베이스 설정
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# 보안 설정
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]  # 실제 도메인 또는 IP 주소로 변경
DEBUG = True  # DEBUG 모드 활성화
