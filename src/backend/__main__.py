import sys

import uvicorn

from src.backend import create_api

SERVER_PORT = 5000
SERVER = "0.0.0.0"
LOG_LEVEL = "debug"


def main() -> None:
    uvicorn.run(create_api(), host=SERVER, port=SERVER_PORT)


if __name__ == "__main__":
    sys.exit(main())
