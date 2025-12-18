import threading
from Jarvis.main import CommandDetector
from Panel.server import run_server



if __name__ == "__main__":
 h1 = threading.Thread(target=run_server, daemon=True).start()
 run = CommandDetector()
 run.main()