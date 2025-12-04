import httpx
import streamlit as st
from retry import retry
from config import settings

@st.cache_data(show_spinner=False, ttl=30)
@retry(
    exceptions=(httpx.ReadTimeout, httpx.HTTPStatusError),
    tries=3,
    delay=1,
    backoff=2,
)
def fetch(endpoint: str):
    """
    Sync wrapper calling FastAPI endpoints via httpx.
    Streamlit does not support native async.
    """
    url = f"{settings.API_URL}{endpoint}"

    r = httpx.get(url, timeout=20)
    r.raise_for_status()
    return r.json()
