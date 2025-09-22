"""
Workout Tracker - Enkel og ren implementasjon
Med Google OAuth og tradisjonell innlogging
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import httpx
from datetime import datetime
from typing import Dict, List

# ============================================================================
# KONFIGURASJON
# ============================================================================

app = FastAPI(title="Workout Tracker", version="1.0.1")

# Static files og templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Google OAuth konfigurasjon
import os
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://your-app-name.vercel.app/auth/google/callback")

# Sjekk at OAuth er konfigurert
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    print("⚠️  Google OAuth ikke konfigurert! Sett miljøvariabler:")
    print("   GOOGLE_CLIENT_ID")
    print("   GOOGLE_CLIENT_SECRET")
    print("   GOOGLE_REDIRECT_URI")

# ============================================================================
# DATA LAGRING
# ============================================================================

workouts: List[Dict] = []
users = {"demo": "demo123"}  # Demo bruker for testing
google_users: Dict = {}
current_user = None

# ============================================================================
# HJELPEFUNKSJONER
# ============================================================================

def get_current_day() -> str:
    """Hent dagens navn på norsk"""
    days = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    return days[datetime.now().weekday()]

def calculate_weekly_streak() -> int:
    """Beregn ukesstreak basert på antall treningsøkter"""
    return len(workouts) // 3  # Enkel beregning

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Innloggingsside"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/auth/google")
async def google_auth():
    """Redirect til Google OAuth"""
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile"
    )
    return RedirectResponse(url=google_auth_url)

@app.get("/auth/google/callback")
async def google_auth_callback(code: str):
    """Håndter Google OAuth callback"""
    try:
        # Bytt kode mot access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_REDIRECT_URI
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status()
            token_info = token_response.json()
            
            # Hent brukerinfo fra Google
            userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {token_info['access_token']}"}
            user_response = await client.get(userinfo_url, headers=headers)
            user_response.raise_for_status()
            user_info = user_response.json()
            
            # Lagre brukerinfo
            google_id = user_info["id"]
            email = user_info["email"]
            name = user_info.get("name", email.split("@")[0])
            
            google_users[google_id] = {
                "email": email,
                "name": name,
                "google_id": google_id
            }
            
            # Sett som aktiv bruker og redirect til hjem
            global current_user
            current_user = name
            return RedirectResponse(url="/home", status_code=303)
            
    except Exception as e:
        print(f"Google OAuth error: {e}")
        return RedirectResponse(url="/?error=oauth_failed", status_code=303)

@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    """Tradisjonell innlogging"""
    if username in users and users[username] == password:
        global current_user
        current_user = username
        return RedirectResponse(url="/home", status_code=303)
    else:
        return RedirectResponse(url="/?error=invalid_credentials", status_code=303)

@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    """Hjemmeside"""
    return templates.TemplateResponse("home.html", {
        "request": request,
        "current_user": current_user,
        "workouts": workouts,
        "current_day": get_current_day(),
        "weekly_streak": calculate_weekly_streak()
    })

@app.post("/add_workout")
async def add_workout(
    workout_type: str = Form(),
    workout_name: str = Form(),
    duration: str = Form(),
    day: str = Form()
):
    """Legg til ny treningsøkt"""
    workout = {
        "type": workout_type,
        "name": workout_name,
        "duration": duration,
        "day": day,
        "timestamp": datetime.now().isoformat()
    }
    workouts.append(workout)
    return RedirectResponse(url="/home", status_code=303)

# ============================================================================
# START APP
# ============================================================================

# For Vercel deployment
app = app

if __name__ == "__main__":
    print("🚀 Starting Workout Tracker...")
    print("📍 URL: http://localhost:5000")
    print("🔐 Google OAuth: Enabled")
    print("👤 Demo login: demo / demo123")
    print("=" * 50)
    
    uvicorn.run(app, host="127.0.0.1", port=5000)
