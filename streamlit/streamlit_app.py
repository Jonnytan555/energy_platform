import streamlit as st
from config import settings
from api_client import login, register, me, logout

st.set_page_config(page_title="Energy Platform", page_icon="⚡", layout="wide")

st.title("⚡ Energy Analytics Platform")
st.caption(f"API: {settings.API_URL}")

token = st.session_state.get("access_token")

with st.sidebar:
    st.header("🔐 Authentication")

    if token:
        st.success("Logged in")
        if st.button("Who am I? (/auth/me)"):
            try:
                st.json(me())
            except Exception as e:
                st.error(str(e))

        if st.button("Logout"):
            logout()
            st.rerun()

    else:
        tab_login, tab_register = st.tabs(["Login", "Register"])

        with tab_login:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pw")
            if st.button("Login"):
                try:
                    login(email, password)
                    st.success("Logged in")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

        with tab_register:
            r_email = st.text_input("Email", key="reg_email")
            r_password = st.text_input("Password", type="password", key="reg_pw")
            if st.button("Register"):
                try:
                    res = register(r_email, r_password)
                    st.success(f"Registered user id={res.get('id')}")
                except Exception as e:
                    st.error(str(e))

st.markdown(
    """
Welcome.

Use the left sidebar to login/register, then open:

- **📦 Storage** (AGSI + ALSI latest-only from DB + scrape + refresh)

"""
)
