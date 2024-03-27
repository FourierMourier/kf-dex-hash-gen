import asyncio
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
import bcrypt
import base64
from fastapi.templating import Jinja2Templates

# --- if uvloop can't be installed, comment the code below:
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# ---

app = FastAPI()


templates = Jinja2Templates(directory=".")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate_hash")
async def generate_hash(password: str = Form(...)):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    encoded_password = base64.b64encode(hashed_password)
    return JSONResponse(
        content={"hashed_password": hashed_password.decode(), "encoded_password": encoded_password.decode()})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
