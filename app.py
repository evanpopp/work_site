import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from altcha import ChallengeOptionsV1, create_challenge_v1, verify_solution_v1

app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
templates = Jinja2Templates(directory="static")

## HMAC Key Setup ##
load_dotenv()
HMAC_KEY = os.environ.get("ALTCHA_HMAC_KEY")
if not HMAC_KEY:
    raise RuntimeError("ALTCHA_HMAC_KEY is not configured. Check your .env file.")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "form.html")

@app.get("/altcha/challenge")
async def altcha_challenge():
    options = ChallengeOptionsV1(
        algorithm="SHA-256",
        hmac_key=HMAC_KEY,
        max_number=100_000,
        expires=datetime.now(timezone.utc) + timedelta(minutes=1),
    )
    challenge = create_challenge_v1(options)
    data = {
        "algorithm": challenge.algorithm,
        "challenge": challenge.challenge,
        "maxnumber": challenge.max_number,
        "salt": challenge.salt,
        "signature": challenge.signature,
    }
    return JSONResponse(data)

@app.post("/home", response_class=HTMLResponse)
async def home(request: Request, altcha: str = Form(...)):
    ok, err = verify_solution_v1(altcha, HMAC_KEY, check_expires=True)
    if not ok:
        return HTMLResponse(
            f"<h1>Verification failed</h1><p>{err}</p>", status_code=400
        )
    return templates.TemplateResponse(request, "index.html")

## Monitor Server ##
@app.head("/health", status_code=200)
async def health_check():
    return {"status": "ok"}

'''
uvicorn app:app --host 0.0.0.0 --port 8000
sudo systemctl restart popps106
'''