import streamlit as st
import pandas as pd


def show_dataframe(data: list, title: str = "", height: int = 400):
    """Render a list-of-dicts as a styled Streamlit dataframe."""
    if not data:
        st.info("No records found.")
        return
    df = pd.DataFrame(data)
    if title:
        st.subheader(title)
    st.dataframe(df, use_container_width=True, height=height)
    return df


def metric_card(label: str, value, delta=None):
    st.metric(label=label, value=value, delta=delta)


def success(msg: str):
    st.success(f"✅ {msg}")


def error(msg: str):
    st.error(f"❌ {msg}")


def page_header(title: str, subtitle: str = ""):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()
