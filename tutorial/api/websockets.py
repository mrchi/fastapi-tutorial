# coding=utf-8

from fastapi import APIRouter
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

router = APIRouter()
html_content = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/websockets/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/", summary="WebSocket test page")
def websocket_page():
    return HTMLResponse(html_content)


@router.websocket("/ws", name="websocket decorator has no summary param")
async def websocket_api(ws: WebSocket):
    """It's NOT shown in docs."""
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Message text was: {data}")
