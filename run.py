import os

CYTHON = "python -m pip install cython"
REQUIREMENTS = "python -m pip install -r requirements.txt"
SERVER = "python server.py"

NPM_INSTALL = f"npm install --prefix {os.path.join(os.getcwd(), 'my-app')}"
NPM_START = f"npm start --prefix {os.path.join(os.getcwd(), 'my-app')}"

def run(command):
    if os.system(command) != 0:
        print(f"Failed to run command {command}")


def handle_server():
    [run(command) for command in [CYTHON, REQUIREMENTS, SERVER]]


def handle_client:
    [run(command) for command in [NPM_INSTALL, NPM_START]]

if __name__ == "__main__":
    if os.fork() == 0:
        handle_client()
    else:
        handle_server()