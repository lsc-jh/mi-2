from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os
import webbrowser
import _thread
from time import sleep
from jsonservice import JsonService
import requests
import json

SERVER_URL = "http://localhost:8000"
AI_URL = "https://lsc-ai.kou-gen.net/api/generate"
service = JsonService('users.json')

class User:
    def __init__(self, username: str, current_scene: str = "start"):
        self.username = username
        self.current_scene = current_scene
        self.scene = {}

    # TODO: Functions
    def generate_next_scene(self, choice=None, model="llama3"):
        choices = list(self.scene.get("choices", {}).values())
        prompt = get_prompt(self.current_scene, choices, "", choice)
        prompt += f"""
    IMPORTANT: Don't include any other message then the JSON format.
    Don't use: "Here's the next scene: <scene description>." or "Choose between: <choice1_text> and <choice2_text>."
    Format:
    {{
      "description": "<scene description>",
      "name": "<scene_name>",
      "choices": {{
        "choice1_key": "<choice1_text>",
        "choice2_key": "<choice2_text>"
      }}
    }}
    """
        print(prompt)

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(AI_URL, json=payload)
        if response.status_code == 200:
            self.scene = json.loads(response.json().get("response"))
            self.current_scene = self.scene["name"]
        else:
            print("Error:", response.text)
            return None

    def serialize(self):
        return{
            "current_scene": self.current_scene,
            "scene": self.scene
        }


def open_browser(*args) -> None:
    sleep(2)
    if os.path.exists("game.html"):
        webbrowser.open_new("game.html")

def get_user(username:str, _users: list[User]):
    for user in _users:
        if user.username == username:
            return user
    return None



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



users = service.read("users") or []

@app.get("/", tags=["Adventure"])
def home():
    return {
        "message": "Hello Adventurer!",
    }

@app.get("/start", tags=["Adventure"])
def start(username: str):
    user = get_user(username, users)
    if not user:
        user = User(username)
        users.append(user)

    user.generate_next_scene()
    return user.scene


class GameChoice(BaseModel):
    username: str
    choice: str

@app.post("/continue", tags=["Adveture"])
def continue_game(game_choice: GameChoice):
    username = game_choice.username
    choice = game_choice.choice

    user= get_user(username, users)
    if not user:
        return {"message": "User not found!"}

    if not user.scene:
        return {"message": "User has not started the game"}

    if choice not in user.scene["choices"]:
        return {"message": "Invalid choice!"}

    user.generate_next_scene(choice)
    return  user.scene


if __name__ == "__main__":
    #_thread.start_new_thread(open_browser, ())
    uvicorn.run("main:app", reload=True)
