import json
import urllib.request
from wsgiref.simple_server import make_server

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/").strip("/")
    if not path:
        status = "400 Bad Request"
        response = {'error': "Currency code is required, e.g. /USD"}
    else:
        currency = path.upper()
        url = f" https://api.exchangerate-api.com/v4/latest/{currency}"
        try:
            with urllib.request.urlopen(url) as resp:
                data = resp.read()
                response = json.loads(data.decode("utf-8"))
            status = "200 OK"
        except Exception as e:
            status = "502 Bad Gateway"
            response = {"error": str(e)}

    body = json.dumps(response).encode("utf-8")
    headers = [("Content-Type", "application/json"), ("Content-Length", str(len(body)))]
    start_response(status, headers)
    return [body]




if __name__ == "__main__":

    print("http://localhost:8000")
    make_server("0.0.0.0", 8000, app).serve_forever()