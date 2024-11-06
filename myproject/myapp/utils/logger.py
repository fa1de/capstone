import logging
import os


# 로거 설정 함수
def set_logger(name, log_file, level=logging.INFO):
    """로그 설정 함수.

    Args:
        name (str): 로거 이름.
        log_file (str): 로그 파일 경로.
        level (int): 로깅 레벨 (디폴트: logging.INFO).
    """
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 파일 핸들러 생성
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)

    # 포맷터 설정
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # 핸들러 로거에 추가
    logger.addHandler(handler)

    return logger


LOG_FILE_PATH = "log/"
LOG_FILE_NAME = "log.txt"


if not os.path.exists(LOG_FILE_PATH):
    os.makedirs(LOG_FILE_PATH)

logger = set_logger("", LOG_FILE_PATH + LOG_FILE_NAME)
