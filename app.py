from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from agent import generate_reply

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/")
def home():
    return {
        "message": "SHL Conversational Recommender API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    messages = [msg.dict() for msg in request.messages]

    result = generate_reply(messages)

    return result