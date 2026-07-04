import streamlit as st

from database_manager.db import clear_history, delete_entry, get_history, search_history


def render_history():
    st.title("🕘 Download History")

    search_term = st.text_input("Search history", placeholder="Search by title or URL...")

    rows = search_history(search_term) if search_term else get_history()

    if not rows:
        st.info("No history yet. Download something first!")
        return

    if st.button("🗑️ Clear All History"):
        clear_history()
        st.rerun()

    for row in rows:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{row['title']}**")
                st.caption(f"{row['platform']} | {row['quality']} | {row['date']} | {row['status']}")
                st.caption(row["location"])
            with col2:
                if st.button("🗑️ Delete", key=f"del_{row['id']}"):
                    delete_entry(row["id"])
                    st.rerun()
