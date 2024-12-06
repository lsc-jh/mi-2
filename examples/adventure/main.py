import json

from fastapi import FastAPI, HTTPException
from pydantic.v1 import BaseModel
from starlette.middleware.cors import CORSMiddleware

SERVER_URL = "http://localhost:8000"
user_states = {}

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
    if user in user_states:
        return {
            "message": f"Welcome back {user}!",
            # TODO: Fix this line
            "scene": scenes[user_states[user]],
        }
    else:
        return {
            "message": f"Welcome {user}!",
            # TODO: Fix this line
            "scene": scenes[user_states[user]]
        }


@app.get("/save", tags=["Adventure"])
def save(user: str):
    if user not in user_states:
        raise HTTPException(status_code=404, detail=f"Game not started for {user}!")
    return {
        "message": f"Game saved for {user}!",
        # TODO: Fix this line
        "current_scene": scenes[user_states[user]],
    }

class GameChoice(BaseModel):
    user: str
    choice: str

@app.post("/continue", tags=["Adventure"])
def continue_game(resp: GameChoice):
    user = resp.user
    choice = resp.choice
