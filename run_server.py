import os
from sys import argv

CYTHON = "python -m pip install cython"
REQUIREMENTS = "python -m pip install -r requirements.txt"
SERVER = "python server.py"

NPM_INSTALL = f"cd {os.path.join(os.getcwd(), 'my-app')} && npm install"
NPM_START = f"npm start --prefix {os.path.join(os.getcwd(), 'my-app')}"


def run(command):
    if os.system(command) != 0:
        print(f"Failed to run command {command}")


def handle_server():
    run(SERVER)

def handle_install():
    [run(command) for command in [CYTHON, REQUIREMENTS]]


if __name__ == "__main__":
    if "no-installation" not in argv:
        handle_install()
    if "no-server" not in argv:
        handle_server()