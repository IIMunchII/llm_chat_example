import os
from typing import Dict, List

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def update_message_history(message: dict[str, str]) -> None:
    message_history.append(message)
    

async def call_gpt(messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo"):
    return openai.ChatCompletion.acreate(
        messages=messages,
        stream=True,
        temperature=0.2,
        model=model,
    )


def get_python_assistant_system_prompt() -> list[dict[str, str]]:
    return create_system_message(
        "You are a helpful coding expert in Python, that always does your best to answer coding related questions using best practices, no comments in code examples and always uses typehints in Python etc."
    )


def create_system_message(content) -> dict[str, str]:
    return {"role": "system", "content": content}


def create_assistant_message(content) -> dict[str, str]:
    return {"role": "assistant", "content": content}


def create_user_message(content) -> dict[str, str]:
    return {"role": "user", "content": content}

message_history = [get_python_assistant_system_prompt()]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("event_type", "") == "#GPT_BEGIN#":
                await websocket.send_text("#GPT_BEGIN#")
                continue
            user_message = create_user_message(data.get("prompt"))
            message_history.append(user_message)
            response = await call_gpt(message_history, data.get("model"))
            content_aggregate = ""
            async for item in await response:
                delta = item["choices"][0]["delta"]
                msg = delta.get("content", "")
                await websocket.send_text(msg)
                content_aggregate += msg
            await websocket.send_text("#GPT_END#")
            update_message_history(create_assistant_message(content_aggregate))

    except WebSocketDisconnect:
        print(f"WebSocket connection closed")
        message_history.clear()



@app.get("/")
async def serve_home():
    with open("index.html", "r") as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
