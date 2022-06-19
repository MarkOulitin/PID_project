import os
from multiprocessing import Process

CYTHON = "python -m pip install cython"
REQUIREMENTS = "python -m pip install -r requirements.txt"
SERVER = "python server.py"

NPM_INSTALL = f"cd {os.path.join(os.getcwd(), 'my-app')} && npm install"
NPM_START = f"npm start --prefix {os.path.join(os.getcwd(), 'my-app')}"

def run(command):
    if os.system(command) != 0:
        print(f"Failed to run command {command}")


def handle_server():
    [run(command) for command in [CYTHON, REQUIREMENTS, SERVER]]


def handle_client():
    [run(command) for command in [NPM_INSTALL, NPM_START]]

if __name__ == "__main__":
    client = Process(target=handle_client)
    server = Process(target=handle_server)
    client.start()
    server.start()
    client.join()
    server.join()