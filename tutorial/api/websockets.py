# coding=utf-8

from typing import Optional
from fastapi import (
    APIRouter,
    Cookie,
    Query,
    status,
    Depends,
    WebSocketDisconnect,
    WebSocket,
)
from starlette.responses import HTMLResponse

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


@router.get("/page1", summary="WebSocket test page")
def websocket_page():
    return HTMLResponse(html_content)


@router.websocket("/ws", name="websocket API")
async def websocket_api(ws: WebSocket):
    """It's NOT shown in docs."""
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Message text was: {data}")


html_content_with_auth = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/websockets/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
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


async def get_cookie_or_token(
    ws: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@router.get(
    "/page2", response_class=HTMLResponse, name="Websocket with dependencies test page"
)
def websocket_page2():
    return HTMLResponse(html_content_with_auth)


@router.websocket("/{item_id}/ws", name="Websocket API with dependencies.")
async def websocket_api_with_dependencies(
    ws: WebSocket,
    item_id: str,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    await ws.accept()
    while True:
        try:
            data = await ws.receive_text()
        except WebSocketDisconnect:
            print("Client disconnected.")
            break
        await ws.send_text(f"Session cookie or query token value is: {cookie_or_token}")
        await ws.send_text(f"Message text was: {data}, for item ID: {item_id}")
