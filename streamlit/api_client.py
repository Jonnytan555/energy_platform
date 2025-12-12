import httpx
import streamlit as st
from retry import retry
from config import settings

def _auth_headers() -> dict:
    token = st.session_state.get("access_token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

@retry(
    exceptions=(httpx.ReadTimeout, httpx.HTTPStatusError),
    tries=3,
    delay=1,
    backoff=2,
)
def api_get(endpoint: str, params: dict | None = None):
    url = f"{settings.API_URL}{endpoint}"
    r = httpx.get(url, params=params, headers=_auth_headers(), timeout=30)
    r.raise_for_status()
    return r.json()

@retry(
    exceptions=(httpx.ReadTimeout, httpx.HTTPStatusError),
    tries=3,
    delay=1,
    backoff=2,
)
def api_post(endpoint: str, payload: dict | None = None, params: dict | None = None):
    url = f"{settings.API_URL}{endpoint}"
    r = httpx.post(url, json=payload, params=params, headers=_auth_headers(), timeout=60)
    r.raise_for_status()
    return r.json()

# -------- Auth --------
def login(email: str, password: str) -> str:
    res = api_post("/auth/login", payload={"email": email, "password": password})
    token = res["access_token"]
    st.session_state["access_token"] = token
    return token

def register(email: str, password: str) -> dict:
    return api_post("/auth/register", payload={"email": email, "password": password})

def me() -> dict:
    return api_get("/auth/me")

def logout():
    st.session_state.pop("access_token", None)

# -------- Storage (DB latest) --------
def fetch_agsi_latest(limit: int = 365):
    # matches backend example: GET /storage/agsi/{zone}/latest?limit=...
    # If your backend is actually /storage/agsi/{zone}/latest, use zone param.
    return api_get("/storage/agsi/eu/latest", params={"limit": limit})

def fetch_alsi_latest(limit: int = 365):
    return api_get("/storage/alsi/latest", params={"limit": limit})

# -------- Storage (Scrape + persist) --------
def scrape_agsi(zone: str = "eu", pages: int | None = 30):
    params = {}
    if pages:
        params["pages"] = pages
    return api_post(f"/storage/agsi/{zone}/scrape", params=params)

def scrape_alsi(country: str = "EU"):
    return api_post("/storage/alsi/scrape", params={"country": country})
