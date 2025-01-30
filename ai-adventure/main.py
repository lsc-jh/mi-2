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
from googletrans import Translator
import asyncio

SERVER_URL = "http://localhost:8000"
AI_URL = "https://lsc-ai.kou-gen.net/api/generate"
PROMPT_URL = "https://lsc-ai.kou-gen.net/prompt/mi-2/v1/generate"

service = JsonService('data.json')

def _insert_scene(_scenes, scene_name, scene_data) -> dict:
    if scene_name in _scenes:
        return _scenes

    if _scenes == {}:
        _scenes[scene_name] = scene_data
        return _scenes

    for key, value in _scenes.items():
        if "scenes" in value:
            if scene_name in value["choices"]:
                value["scenes"][scene_name] = scene_data
                return  _scenes
            else:
                _insert_scene(value["scenes"], scene_name, scene_data)
                return _scenes
        else:
            if scene_name in value["choices"]:
                value["scenes"] = {scene_name:scene_data}
                return _scenes
def _find_scene(_scenes, scene_name):
    if scene_name in _scenes:
        return _scenes[scene_name]

    for key,value in _scenes.items():
        if "scenes" in value:
            result = _find_scene(value["scenes"], scene_name)
            if result:
                return result
    return None

class Scenes:
    def __init__(self):
        scenes_data = service.read("scenes")
        if scenes_data:
            self.scenes = scenes_data
        else:
            self.scenes = {}

    def insert_scene(self, current_scene, new_scene):
        _scenes = _insert_scene(self.scenes, current_scene, new_scene)
        self.scenes = _scenes
        service.write("scenes", self.scenes)

    def find_scene(self, scene_name):
        return _find_scene(self.scenes, scene_name)

scenes = Scenes()

class User:
    def __init__(self, username: str, json_data=None):
        self.username = username

        if json_data:
            self.current_scene = json_data["current_scene"]
            self.scene_count = json_data["scene_count"]
            self.max_scenes = json_data.get("max_scenes", 10)
            self.scene = json_data["scene"]

        else:
            self.current_scene = "start"
            self.scene_count = 0
            self.max_scenes = 10
            self.scene = {}

    def generate_next_scene(self, scene_name = None, choice=None):
        if self.scene_count >= self.max_scenes:
            return

        self.scene_count += 1

        if scene_name:
            self.current_scene = scene_name
            self.scene = scenes.find_scene(scene_name)
            if self.scene:
                service.write(f"users.{self.username}", self.serialize())
                return
            else:
                self.scene = {}

        choices = list(self.scene.get("choices", {}).values())
        body = {
            "scene": self.current_scene,
            "choices": choices,
            "context": self.scene.get("description", ""),
            "choice": choice,
            "scene_count": self.scene_count,
            "max_scenes": self.max_scenes
        }
        prompt_res = requests.post(PROMPT_URL, json=body)

        if prompt_res.status_code == 200:
            raw_json = prompt_res.json()
            prompt = raw_json.get("prompt")
        else:
            print("Error:", prompt_res.text)
            return None

        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(AI_URL, json=payload)

        try:
            if response.status_code == 200:
                self.scene = json.loads(response.json().get("response"))
                self.current_scene = self.scene["name"]

                scenes.insert_scene(self.current_scene, self.scene)

                service.write(f"users.{self.username}", self.serialize())
            else:
                print("Error:", response.text)
                return None
        except:
            print("Error:", response.text)
            return

    # NOTE: This method is for saving the user in JSON format
    def serialize(self, custom_scene = None):
        return {
            "current_scene": self.current_scene,
            "scene_count": self.scene_count,
            "max_scenes": self.max_scenes,
            "scene": self.scene if not custom_scene else custom_scene
        }


# NOTE: This method already exists in the main.py file
def open_browser():
    sleep(2)
    if os.path.exists("game.html"):
        webbrowser.open_new("game.html")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Adventure"])
def home():
    return {
        "message": "Hello Adventurer!",
    }

@app.get("/scenes", tags=["Adventure"])
def list_scenes():
    scene_names = [s["name"] for s in scenes.scenes.values()]
    return{
        "scenes": scene_names
    }


@app.get("/start", tags=["Adventure"])
async def start(username: str, max_scenes: int = 10, language: str = "en"):
    user = service.read(f"users.{username}")

    if not user:
        user = User(username)
        user.max_scenes = max_scenes
        service.write(f"users.{username}", user.serialize())
        user.generate_next_scene()
    else:
        user = User(username, user)

    #if language!="en":
    #    return await user.translate_scene(language)

    return user.scene


class GameChoice(BaseModel):
    username: str
    choice: str


@app.post("/continue", tags=["Adventure"])
def continue_game(game_choice: GameChoice):
    username = game_choice.username
    choice = game_choice.choice

    user = service.read(f"users.{username}")

    if not user:
        return {"message": "User not found!"}

    user = User(username, user)

    if not user.scene:
        return {"message": "User scene not found! Go to /start"}

    if choice not in user.scene["choices"]:
        return {"message": "Invalid choice!"}

    user.generate_next_scene(choice)

    return user.scene


if __name__ == "__main__":
    #_thread.start_new_thread(open_browser, ())  # Don't worry about this warning.
    uvicorn.run("main:app", reload=True)
