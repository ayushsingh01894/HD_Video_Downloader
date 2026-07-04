import streamlit as st

from config import APP_NAME, DOWNLOAD_DIR, STYLE_PATH
from database_manager.db import init_db
from ui.footer import render_footer
from ui.history import render_history
from ui.home import render_home
from ui.sidebar import render_sidebar

st.set_page_config(page_title=APP_NAME, page_icon="🎬", layout="wide")

init_db()

if STYLE_PATH.exists():
    with open(STYLE_PATH, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

page = render_sidebar()

if page == "Home":
    render_home()
elif page == "History":
    render_history()
elif page == "Settings":
    st.title("⚙️ Settings")
    st.text_input("Default download folder", value=str(DOWNLOAD_DIR), disabled=True)
    st.selectbox("Default quality", ["best", "1080p", "720p", "480p", "360p", "Audio only"], index=0)
    st.selectbox("Theme", ["dark", "light"], index=0)
    st.checkbox("Auto-open folder after download", value=False)
    st.number_input("History limit", min_value=10, max_value=1000, value=200, step=10)
    st.number_input("Download threads", min_value=1, max_value=4, value=1)
    st.info(
        "These settings are currently informational. Wire them into config.py "
        "(and re-read them in app.py) if you want them to persist across runs."
    )
elif page == "About":
    st.title("ℹ️ About")
    st.write(f"**{APP_NAME}**")
    st.write("Built with Streamlit and yt-dlp.")
    st.warning(
        "This tool is intended for downloading videos you own, that are public "
        "domain, or that you otherwise have permission to download. Downloading "
        "copyrighted content without permission may violate a platform's Terms "
        "of Service and copyright law."
    )

render_footer()
