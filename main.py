# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

import argparse

import uvicorn
from fastapi import FastAPI

from src.config import container
from src.converter import requestconverter, responseconverter
from src.presentation.api.playerapi import router

app: FastAPI = FastAPI()

app.include_router(router)


def wire(url_env: str) -> None:
    app.state.container = container
    app.state.container.config.from_dict(
        {
            "url_env": url_env,
            "routes": {route.name: route.path for route in router.routes},
            "name": "",
            "method": "",
        }
    )
    app.state.container.wire(modules=[requestconverter, responseconverter])


def unwire() -> None:
    app.state.container.unwire()


def run(port: int) -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MicroChess Player")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind socket of Player")
    parser.add_argument("--url_env", type=str, help="URL of MicroChess Environment API server")

    args = parser.parse_args()
    wire(args.url_env)
    run(args.port)
