
import streamlit as st

# Page setup must come first
st.set_page_config(page_title="Sandbox-Based Document Generator", layout="wide")

# -------- Sidebar Login Button (Top-Left) --------
with st.sidebar:
    if st.button("🔐 Login", key="sidebar_login"):
        st.session_state["auth_page"] = "login"
        st.switch_page("pages/Auth.py")  # Ensure Auth.py is inside /pages folder

# -------- App Heading --------
st.markdown("<h1 style='color:#00B4D8;'>📄 Sandbox-Based Document Generator 🚀</h1>", unsafe_allow_html=True)

st.markdown("""
Welcome to the intelligent document generation platform powered by AI.

Use the navigation in the sidebar to:
- `Auth`: Log in or sign up
- `Document Uploader`: Upload your `.txt`, `.csv`, `.xlsx`, `.mdv` files
- `Template Mapping`: Map sections and preview your final document
""")
