from fastapi import FastAPI
from typing import Literal
import wikipedia
from chatbot import Chat

tags_metadata = [
    {
        "name": "Demo",
        "description": "API endpoints for demo purposes",
    },
    {
        "name": "Home",
        "description": "Basic endpoints"
    },
    {
        "name": "AI",
        "description": "AI operations"
    }
]

app = FastAPI(
    openapi_tags=tags_metadata,
)

@app.get("/", tags=["Home"])
def home():
    return {"message": "Hello World!"}

@app.get("/about", tags=["Home"])
def about():
    return {
        "Author": "Joshua Hegedus @ home",
        "Type": "Logiscool Project",
        "Description": "An AI API collection."
    }

@app.get("/calculate", tags=["Demo"])
def calculate(a: int, b: int):
    result = a + b

    return {
        "a": a,
        "b": b,
        "result": result
    }

@app.get("/calculate/{a}/{b}", tags=["Demo"])
def complex_calculate(a: int, b: int, operator: Literal["+", "-", "*", "/"] = "+"):

    match operator:
        case "+":
            result = a + b
        case "-":
            result = a - b
        case "*":
            result = a * b
        case "/":
            result = a / b

    return {
        "a": a,
        "b": b,
        "operator": operator,
        "result": result if result else "Some of the input were incorrect!"
    }

from pydantic import BaseModel

class CalcReqeust(BaseModel):
    a: int
    b: int
    operator: str = "+"

@app.post("/calculate", tags=["Demo"])
def caluclate_post(req: CalcReqeust):
    a, b, operator = req.a, req.b, req.operator

    if operator == "+":
        result = a + b
    elif operator == "-":
        result = a - b
    elif operator == "*":
        result = a * b
    elif operator == "/":
        result = a / b

    return {
        "a": a,
        "b": b,
        "operator": operator,
        "result": result if result else "Some of the input were incorrect!"
    }


class AIOperation(BaseModel):
    text: str

class ChatRequest(AIOperation):
    user: str


@app.post("/ai/summary", tags=["AI"])
def ai_summary(req: AIOperation):
    return {"text": req.text}


@app.get("/ai/wikipedia/search", tags=["AI"])
def wikipedia_search(search_term: str, lang: str = "en"):
    wikipedia.set_lang(lang)
    try:
        results = wikipedia.search(search_term)
    except wikipedia.exceptions.DisambiguationError as e:
        results = e.options
    if len(results) == 0:
        return {
            "search_term": search_term,
            "result": "No results found"
        }
    if results[0] == search_term:
        try:
            page = wikipedia.page(results[0])
        except wikipedia.exceptions.DisambiguationError as e:
            return {
                "search_term": search_term,
                "result": e.options
            }
        except wikipedia.exceptions.PageError as e:
            return {
                "search_term": search_term,
                "result": "No results found"
            }
        return {
            "search_term": search_term,
            "result": page.content
        }

    return {
        "search_term": search_term,
        "result": results
    }

chats = {}  # type: dict[str, Chat]

def get_or_create_chat(user_name: str) -> Chat:
    pass

@app.post("/ai/chat", tags=["AI"])
def ai_chat(req: ChatRequest):
    chat = get_or_create_chat(req.user)
    return chat.respond(req.text)