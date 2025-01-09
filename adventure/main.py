import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

import uvicorn
import os
import webbrowser
import _thread
from time import sleep
from jsonservice import JsonService


def abs_path(rel_path: str) -> str:
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dir_name, rel_path))

def open_browser():
    sleep(2)
    current_path = abs_path(WEBPAGE_URL)
    if os.path.exists(current_path):
        webbrowser.open_new(current_path)


WEBPAGE_URL = "game.html"
SERVER_URL = "http://localhost:8000"
service = JsonService('users.json')

user_states = service.read("users") if service.read("users") else {}

with open('scenes.json', 'r') as f:
    scenes = json.load(f)

# TODO: Improve the description
description = """The backend for an adventure game.

## Story
- ...
"""

app = FastAPI(
    description=description
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with a list of origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Adventure"])
def home():
    return {
        "message": "Hello Adventurer!",
        "possible_routes": [
            f"GET;{SERVER_URL}/start;Start Game",
            f"POST;{SERVER_URL}/continue;Continue Game",
            f"GET;{SERVER_URL}/save;Save Game",
            f"GET;{SERVER_URL}/load;Load Game"
        ]
    }

@app.get("/start", tags=["Adventure"])
def start(user: str):

    if user is None or user == "" or user == "null":
        raise HTTPException(status_code=400, detail="Please enter a valid user name")

    _users = service.read("users") or []
    if user not in user_states and user not in _users:
        user_states[user] = "start"
        service.write(f'users.{user}', "start")
        return {
            "message": f"Welcome {user}!",
            "scene": scenes["start"],
        }


    return {
            "message": f"Welcome back {user}!",
            "scene": scenes[user_states[user]]
        }


@app.get("/save", tags=["Adventure"])
def save(user: str):
    if user not in user_states:
        raise HTTPException(status_code=404, detail=f"Game not started for {user}!")
    service.write(f'users.{user}', user_states[user])
    return {
        "message": f"Game saved for {user}!",
        "current_scene": scenes[user_states[user]]
    }

class GameChoice(BaseModel):
    user: str
    choice: str

@app.post("/continue", tags=["Adventure"])
def continue_game(resp: GameChoice):
    user = resp.user
    choice = resp.choice

    if user not in user_states:
        raise HTTPException(status_code=404, detail=f"Game not started for {user}")

    current_scene = scenes[user_states[user]]

    if choice not in current_scene["choices"]:
        error = {
            "message": f"Choice {choice} is not valid!",
            "possible_choices": current_scene["choices"]
        }
        raise HTTPException(status_code=404, detail=error)

    user_states[user] = choice

    return {
        "message": "Success",
        "scene": scenes[choice]
    }

if __name__ == "__main__":
    _thread.start_new_thread(open_browser, ())
    uvicorn.run("main:app", reload=True)