from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os
import webbrowser
import _thread
from time import sleep
from jsonservice import JsonService
import requests

class User:
    def __init__(self, username: str, current_scene: str = "start"):
        self.username = username
        self.current_scene = current_scene
        self.scene = {}

    # TODO: Functions


def open_browser(*args) -> None:
    sleep(2)
    if os.path.exists("game.html"):
        webbrowser.open_new("game.html")


SERVER_URL = "http://localhost:8000"
AI_URL = "https://lsc-ai.kou-gen.net/api/generate"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


service = JsonService('users.json', default_data={"users": []})
users = service.read("users") or []

@app.get("/", tags=["Adventure"])
def home():
    return {
        "message": "Hello Adventurer!",
    }

if __name__ == "__main__":
    _thread.start_new_thread(open_browser, ())
    uvicorn.run("main:app", reload=True)