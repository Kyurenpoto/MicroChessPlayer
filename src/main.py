# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import argparse

import uvicorn
from fastapi import FastAPI

from src.config import Container
from src.presentation.api import playerapi

app: FastAPI = FastAPI()

app.include_router(playerapi.router)


def wire(url_env: str) -> None:
    app.state.container = Container()
    app.state.container.config.from_dict(
        {"url_env": url_env, "routes": {route.name: route.path for route in playerapi.router.routes}}
    )
    app.state.container.wire(modules=[playerapi])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MicroChess API Server")

    parser.add_argument("--port", type=int, default=8000, help="Port to bind socket of API server")
    parser.add_argument("--url_env", type=str, help="URL of MicroChess Environment API server")

    args = parser.parse_args()

    wire(args.url_env)

    uvicorn.run("main:app", host="0.0.0.0", port=args.port)
