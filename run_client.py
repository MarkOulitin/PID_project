import os
from sys import argv

NPM_INSTALL = f"cd {os.path.join(os.getcwd(), 'my-app')} && npm install"
NPM_START = f"npm start --prefix {os.path.join(os.getcwd(), 'my-app')}"


def run(command):
    if os.system(command) != 0:
        print(f"Failed to run command {command}")

def handle_client():
    run(NPM_START)

def handle_install():
    run(NPM_INSTALL)


if __name__ == "__main__":
    if "no-installation" not in argv:
        handle_install()
    if "no-client" not in argv:
        handle_client()