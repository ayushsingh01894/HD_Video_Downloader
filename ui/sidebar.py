import streamlit as st

from config import APP_NAME


def render_sidebar():
    with st.sidebar:
        st.markdown(f"## 🎬 {APP_NAME}")
        st.markdown("---")
        page = st.radio(
            "Navigation",
            ["Home", "History", "Settings", "About"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.caption("Built with Streamlit + yt-dlp")
        return page
