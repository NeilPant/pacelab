import os

import uvicorn


def run() -> None:
    uvicorn.run(
        "pacelab_server.app:create_app",
        factory=True,
        host=os.environ.get("PACELAB_HOST", "127.0.0.1"),
        port=int(os.environ.get("PACELAB_PORT", "8000")),
    )
