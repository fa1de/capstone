import logging
import signal
from handlers import sigint_handler
from utils import start_server

B_SERVER_ADDRESS = "127.0.0.1"
B_SERVER_PORT = 8002

logging.basicConfig(
    filename="packet_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s"
)

django_server_url = "http://127.0.0.1:8000"

# 패턴을 저장할 리스트
patterns = []


if __name__ == "__main__":
    print(f"run server address: {B_SERVER_ADDRESS}, port: {B_SERVER_PORT}")

    signal.signal(signal.SIGINT, sigint_handler)
    start_server(patterns)
