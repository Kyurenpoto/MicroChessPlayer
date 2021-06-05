# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: GPL-3.0-only

import argparse

import uvicorn
from fastapi import FastAPI

from presentation.api.playerapi import router, setting

app: FastAPI = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MicroChess API Server")

    parser.add_argument("--port", type=int, default=8000, help="Port to bind socket of API server")
    parser.add_argument("--url_env", type=str, help="URL of MicroChess Environment API server")

    args = parser.parse_args()

    setting(args.url_env)

    uvicorn.run("main:app", host="0.0.0.0", port=args.port)
