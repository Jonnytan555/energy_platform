import streamlit as st
import httpx
from jose import jwt
from config import settings

st.title("🔐 Login")

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

def get_claims():
    token = st.session_state.get("access_token")
    if not token:
        return None
    try:
        return jwt.get_unverified_claims(token)
    except Exception:
        return None

email = st.text_input("Email")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

if login_button:
    if not email or not password:
        st.error("Please enter email and password.")
    else:
        try:
            url = f"{settings.API_URL}/auth/login"
            r = httpx.post(url, json={"email": email, "password": password}, timeout=20)
            if r.status_code != 200:
                st.error(f"Login failed: {r.json().get('detail', 'Unknown error')}")
            else:
                st.session_state["access_token"] = r.json()["access_token"]
                st.success("Logged in successfully.")
        except Exception as exc:
            st.error(f"Login error: {exc}")

token = st.session_state.get("access_token")
claims = get_claims()

if token and claims:
    st.info(f"Logged in as: **{claims.get('sub')}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Refresh token"):
            try:
                url = f"{settings.API_URL}/auth/refresh"
                r = httpx.post(
                    url,
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=20,
                )
                r.raise_for_status()
                st.session_state["access_token"] = r.json()["access_token"]
                st.success("Token refreshed.")
            except Exception as exc:
                st.error(f"Failed to refresh token: {exc}")
    with col2:
        if st.button("Logout"):
            st.session_state["access_token"] = None
            st.success("Logged out.")
else:
    st.info("Not logged in.")
