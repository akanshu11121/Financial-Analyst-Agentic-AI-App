import streamlit as st

def styled_button(label, key=None, on_click=None, args=None, kwargs=None, type="primary"):
    """Creates a styled button with custom CSS classes."""
    if type == "primary":
        st.button(label, key=key, on_click=on_click, args=args, kwargs=kwargs, use_container_width=True)
    elif type == "reset":
        st.markdown(
            f"<button class='reset-btn' onclick='{on_click}'>{label}</button>",
            unsafe_allow_html=True
        )

def styled_download_button(label, data, file_name, mime, key=None, type="primary"):
    """Creates a styled download button."""
    st.download_button(label, data, file_name, mime, key=key, use_container_width=True)
