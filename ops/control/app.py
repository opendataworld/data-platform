import os
import subprocess
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

COMPOSE_DIR = os.environ.get("COMPOSE_DIR", "/app/target")
COMPOSE_PROFILES = os.environ.get("COMPOSE_PROFILES", "")

app = FastAPI()
STATIC = Path(__file__).parent / "static"


def _compose(*args: str) -> dict:
    cmd = ["docker", "compose"]
    for p in filter(None, COMPOSE_PROFILES.split(",")):
        cmd += ["--profile", p.strip()]
    cmd += list(args)
    r = subprocess.run(cmd, cwd=COMPOSE_DIR, capture_output=True, text=True)
    return {"cmd": " ".join(cmd), "cwd": COMPOSE_DIR,
            "code": r.returncode, "stdout": r.stdout, "stderr": r.stderr}


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.post("/deploy")
def deploy():
    return JSONResponse(_compose("up", "-d", "--pull", "always"))


@app.post("/stop")
def stop():
    return JSONResponse(_compose("down"))


@app.get("/status")
def status():
    r = _compose("ps", "--format", "json")
    return JSONResponse(r)
