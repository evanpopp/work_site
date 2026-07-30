import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from starlette.middleware.base import BaseHTTPMiddleware

from altcha import ChallengeOptionsV1, create_challenge_v1, verify_solution_v1

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Protects against Clickjacking by preventing your site from being put in an iframe
        response.headers["X-Frame-Options"] = "DENY"
        
        # Prevents the browser from guessing file types (MIME-sniffing)
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Forces HTTPS for one year (31536000 seconds) including subdomains
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Controls where resources can be loaded from
        # Note: We explicitly allow https://cdn.jsdelivr.net so your ALTCHA widget loads correctly
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:;"
            "worker-src 'self' blob:;"
        )
        
        # Controls how much referrer information is passed when routing away from your site
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response

app = FastAPI()
app.mount("/public", StaticFiles(directory="public", html=False), name="public")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/resume", StaticFiles(directory="resume"), name="resume")
templates = Jinja2Templates(directory="static")
app.add_middleware(SecurityHeadersMiddleware)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

## HMAC Key Setup ##
load_dotenv()
HMAC_KEY = os.environ.get("ALTCHA_HMAC_KEY")
if not HMAC_KEY:
    raise RuntimeError("ALTCHA_HMAC_KEY is not configured. Check your .env file.")

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        request, 
        "404.html", 
        status_code=404
    )

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "form.html")

@app.get("/home", response_class=HTMLResponse)
async def form_redirect(request: Request):
    # 307 Temporary Redirect preserves the HTTP method (e.g., POST stays POST)
    return RedirectResponse(url="/", status_code=307)

@app.get("/altcha/challenge")
@limiter.limit("10/minute")  # Limits visitors to 10 challenges per minute
async def altcha_challenge(request: Request):
    options = ChallengeOptionsV1(
        algorithm="SHA-256",
        hmac_key=HMAC_KEY,
        max_number=500_000,
        expires=datetime.now(timezone.utc) + timedelta(minutes=10),
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

@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse("static/robots.txt")

@app.post("/home", response_class=HTMLResponse)
async def home(request: Request, altcha: str = Form(None)):
    if not altcha:
        return templates.TemplateResponse(
            request, 
            "form.html", 
            {"error_message": "Verification required. Please complete the check."}
        )
    ok, err = verify_solution_v1(altcha, HMAC_KEY, check_expires=True)
    if not ok:
        if (err == 'Altcha payload expired'):
            return templates.TemplateResponse(request, "form.html", {"error_message": "Verification expired. Please try again."})
        else:
            return templates.TemplateResponse(
                request, 
                "form.html", 
                {"error_message": f"Verification failed: {err}"}
            )
    return templates.TemplateResponse(request, "index.html")

## Monitor Server ##
@app.head("/health", status_code=200)
async def health_check():
    return {"status": "ok"}

'''
uvicorn app:app --host 127.0.0.1 --port 8001
uvicorn app:app --host 0.0.0.0 --port 8001
sudo systemctl restart evanpopp
'''