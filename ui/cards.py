import streamlit as st

from utils.helper import format_duration, format_number, format_size


def render_video_card(video):
    col1, col2 = st.columns([1, 2])
    with col1:
        if video.thumbnail:
            st.image(video.thumbnail, use_container_width=True)
    with col2:
        st.subheader(video.title)
        st.write(f"**Uploader:** {video.uploader}")
        st.write(f"**Platform:** {video.platform}")
        st.write(f"**Duration:** {format_duration(video.duration)}")
        if video.view_count:
            st.write(f"**Views:** {format_number(video.view_count)}")
        if video.like_count:
            st.write(f"**Likes:** {format_number(video.like_count)}")
        if video.upload_date:
            st.write(f"**Uploaded:** {video.upload_date}")


def render_format_table(video):
    if not video.formats:
        st.info("No detailed format info available for this video.")
        return
    data = [
        {
            "Resolution": f.resolution,
            "Ext": f.ext,
            "Size": format_size(f.filesize),
            "Video codec": f.vcodec,
            "Audio codec": f.acodec,
            "Note": f.note,
        }
        for f in video.formats
    ]
    st.dataframe(data, use_container_width=True)
