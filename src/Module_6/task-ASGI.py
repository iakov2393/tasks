import json
import asyncio
import urllib.request
from functools import partial
import uvicorn

async def app(scope, receive, send):
    if scope["type"] != "http":
        return

    path = scope["path"].strip("/")
    if not path:
        status = 400
        response = {'error': "Currency code is required, e.g. /USD"}
    else:
        currency = path.upper()
        url = f" https://api.exchangerate-api.com/v4/latest/{currency}"
    try:
        loop = asyncio.get_event_loop()
        fetch = partial(urllib.request.urlopen, url)
        with await loop.run_in_executor(None, fetch) as resp:
            data = resp.read()
            response = json.loads(data.decode("utf-8"))
        status = 200
    except Exception as e:
        status = 502
        response = {"error": str(e)}

    body = json.dumps(response).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode()),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})




if __name__ == "__main__":

    print("http://localhost:8000")
    uvicorn.run("task-ASGI:app", host="0.0.0.0", port=8000, reload=False)