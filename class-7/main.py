from fastapi import FastAPI
from typing import Literal

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World!"}

@app.get("/about")
def about():
    return {
        "Author": "Joshua Hegedus",
        "Type": "Logiscool Project",
        "Description": "An AI API collection."
    }

@app.get("/calculate")
def calculate(a: int, b: int):
    result = a + b

    return {
        "a": a,
        "b": b,
        "result": result
    }

@app.get("/calculate/{a}/{b}")
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

@app.post("/calculate")
def caluclate_post(req: CalcReqeust):
    a, b, operator = req.a, req.b, req.operator

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

