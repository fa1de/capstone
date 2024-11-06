import logging
import signal
from .handlers import sigint_handler
from .handlers import start_server

BASE_IP = "127.0.0.1"
ROUTER_PORT = 8002

logging.basicConfig(
    filename="packet_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s"
)

django_server_url = "http://127.0.0.1:8000"

# 패턴을 저장할 리스트
if __name__ == "__main__":
    print(f"run server address: {BASE_IP}, port: {ROUTER_PORT}")

    signal.signal(signal.SIGINT, sigint_handler)
    start_server()
