def sigint_handler(signal, frame):
    print("Received SIGINT, shutting down server...")
    print(f"signal, frame: {signal}, {frame}")
    exit(0)
