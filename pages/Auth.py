import streamlit as st
from utils.auth import init_db, create_user, authenticate_user

# Setup page
st.set_page_config(page_title="Auth", page_icon="🔐")
st.title("🔐 User Authentication")

# Initialize DB
init_db()

# Handle login/logout state
if "logged_in_user" in st.session_state:
    st.success(f"✅ Logged in as **{st.session_state['logged_in_user']}**")
    if st.button("🔓 Logout"):
        st.session_state.pop("logged_in_user")
        st.session_state.pop("auth_page", None)
        st.success("You’ve been logged out.")
        st.stop()

# Detect URL param and update auth_page state
if "signup" in st.query_params:
    st.session_state["auth_page"] = "signup"
elif "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "login"

# Use current state to show correct form
auth_mode = st.session_state["auth_page"]

# 🎨 Layout container
with st.container():
    if auth_mode == "login":
        st.subheader("🔐 Login to Your Account")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type='password', key="login_pass")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.success(f"✅ Welcome back, {username}!")
                st.session_state["logged_in_user"] = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

        # 🧭 Sign-up toggle
        st.markdown("""
            <p style="margin-top: 10px;">
                New user? <a href="?signup=true">Sign up here</a>
            </p>
        """, unsafe_allow_html=True)

    elif auth_mode == "signup":
        st.subheader("🆕 Create a New Account")

        new_user = st.text_input("Choose a Username", key="signup_user")
        new_pass = st.text_input("Choose a Password", type='password', key="signup_pass")

        if st.button("Sign Up"):
            if create_user(new_user, new_pass):
                st.success("🎉 Account created! Please log in.")
                st.session_state["auth_page"] = "login"
                st.rerun()
            else:
                st.error("⚠️ Username already exists or error occurred.")

        # 🧭 Login toggle
        st.markdown("""
            <p style="margin-top: 10px;">
                Already have an account? <a href="?login=true">Login here</a>
            </p>
        """, unsafe_allow_html=True)

# Handle ?login=true link
if "login" in st.query_params:
    st.session_state["auth_page"] = "login"
    st.rerun()
