import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="School ERP System",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports after config ──────────────────────────────────────────────────────
from pages import (
    dashboard,
    student_management,
    attendance_management,
    fee_management,
    result_management,
)

# ── Sidebar navigation ────────────────────────────────────────────────────────
MENU = {
    "🏠 Dashboard": dashboard,
    "👨‍🎓 Student Management": student_management,
    "📅 Attendance Management": attendance_management,
    "💰 Fee Management": fee_management,
    "📝 Result Management": result_management,
}

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/school.png", width=80)
    st.title("School ERP")
    st.caption("Mini School Management System")
    st.divider()
    choice = st.radio("Navigate", list(MENU.keys()), label_visibility="collapsed")
    st.divider()
    st.caption("Built with 🐍 Python + Streamlit\nby a B.Sc CS Student")

# ── Render selected page ──────────────────────────────────────────────────────
MENU[choice].show()
