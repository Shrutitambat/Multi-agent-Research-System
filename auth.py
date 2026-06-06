"""
auth.py — Google OAuth 2.0 for ResearchMind
NO google-auth-oauthlib Flow (causes PKCE/code_verifier bug in Streamlit)
Uses plain requests.post() for token exchange instead.
"""

import os
import requests as req
import streamlit as st
from urllib.parse import urlencode
from google.oauth2 import id_token
from google.auth.transport import requests as g_req

os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

AUTH_URI  = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
SCOPES    = "openid email profile"


def _s(key):
    try:
        v = st.secrets[key]
        if v and not str(v).startswith("YOUR_"):
            return str(v)
    except Exception:
        pass
    return os.environ.get(key, "")

def _client_id():     return _s("GOOGLE_CLIENT_ID")
def _client_secret(): return _s("GOOGLE_CLIENT_SECRET")
def _redirect_uri():
    v = _s("REDIRECT_URI")
    return v or "http://localhost:8501"

def _configured():
    c = _client_id()
    return bool(c and not c.startswith("YOUR_"))


def get_auth_url() -> str:
    """Build Google login URL — NO PKCE, plain OAuth2."""
    if not _configured():
        return "#"
    return AUTH_URI + "?" + urlencode({
        "client_id":     _client_id(),
        "redirect_uri":  _redirect_uri(),
        "response_type": "code",
        "scope":         SCOPES,
        "access_type":   "offline",
        "prompt":        "select_account",
    })


def handle_callback() -> bool:
    """
    Detects ?code= in URL, exchanges it for tokens, stores user in session.
    Returns True on success.
    """
    if not _configured():
        return False

    code  = st.query_params.get("code")
    error = st.query_params.get("error")

    if error:
        st.error(f"Google login error: {error}")
        st.query_params.clear()
        return False

    if not code:
        return False  # Normal page load — no OAuth callback

    try:
        # Direct POST — no Flow object, no PKCE, no state to lose on rerun
        resp = req.post(TOKEN_URI, data={
            "code":          code,
            "client_id":     _client_id(),
            "client_secret": _client_secret(),
            "redirect_uri":  _redirect_uri(),
            "grant_type":    "authorization_code",
        }, timeout=15)

        data = resp.json()

        if "error" in data:
            st.error(f"Token error: {data.get('error_description', data['error'])}")
            st.query_params.clear()
            return False

        id_tok = data.get("id_token", "")
        if not id_tok:
            st.error("No id_token in Google response.")
            st.query_params.clear()
            return False

        # Verify token and extract user info
        info = id_token.verify_oauth2_token(
            id_tok,
            g_req.Request(),
            _client_id(),
            clock_skew_in_seconds=10,
        )

        # Store in Streamlit session
        st.session_state["authenticated"] = True
        st.session_state["user_name"]     = info.get("name", "User")
        st.session_state["user_email"]    = info.get("email", "")
        st.session_state["user_picture"]  = info.get("picture", "")

        st.query_params.clear()
        return True

    except Exception as e:
        st.error(f"Auth error: {e}")
        st.query_params.clear()
        return False


def is_authenticated() -> bool:
    return bool(st.session_state.get("authenticated", False))


def logout():
    for k in ["authenticated", "user_name", "user_email", "user_picture"]:
        st.session_state.pop(k, None)
    st.rerun()


def require_auth():
    """Place at very top of pages/app.py to block unauthenticated access."""
    if not is_authenticated():
        st.markdown("""
        <style>
        html,body,[class*="css"]{background:#040711!important;}
        #MainMenu,footer,header{visibility:hidden!important;}
        </style>
        <div style="position:fixed;inset:0;background:#040711;display:flex;
                    flex-direction:column;align-items:center;justify-content:center;
                    font-family:sans-serif;gap:1rem;z-index:9999;">
            <div style="font-size:2.5rem;">🔒</div>
            <div style="color:#e8eaf6;font-size:1.1rem;font-weight:600;">Authentication Required</div>
            <div style="color:#7b82a0;font-size:.85rem;">Redirecting to login...</div>
            <div style="width:200px;height:3px;background:rgba(123,92,255,.15);
                        border-radius:2px;overflow:hidden;margin-top:.5rem;">
                <div style="height:100%;background:linear-gradient(90deg,#7b5cff,#00c8ff);
                            animation:p 1.2s ease forwards;"></div>
            </div>
        </div>
        <style>@keyframes p{from{width:0}to{width:100%}}</style>
        <script>setTimeout(()=>{ window.location.href='/'; },1300);</script>
        """, unsafe_allow_html=True)
        st.stop()