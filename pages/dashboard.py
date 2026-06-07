import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.db import run_query
from utils.helpers import page_header
 
TOTAL_FEE_PER_STUDENT = 50000
 
 
def kpi_data():
    rows = run_query("""
        SELECT
            (SELECT COUNT(*) FROM students) AS total_students,
            (SELECT COALESCE(SUM(amount),0) FROM fee_payments) AS total_collected,
            (SELECT COUNT(*) FROM attendance WHERE status='Present') AS total_present,
            (SELECT COUNT(*) FROM attendance) AS total_classes
    """)
    return rows[0] if rows else {}
 
 
def top_students(limit=5):
    return run_query(
        """SELECT s.name,
                  ROUND(100.0 * SUM(r.marks_obtained) / NULLIF(SUM(r.max_marks),0), 2) AS avg_percentage
           FROM results r
           JOIN students s ON s.student_id = r.student_id
           GROUP BY s.student_id, s.name
           ORDER BY avg_percentage DESC
           LIMIT %s;""",
        (limit,),
    )
 
 
def attendance_summary():
    return run_query(
        """SELECT sub.subject_name,
                  COUNT(*) AS total,
                  SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) AS present,
                  ROUND(100.0 * SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct
           FROM attendance a
           JOIN subjects sub ON sub.subject_id = a.subject_id
           GROUP BY sub.subject_name
           ORDER BY pct DESC;"""
    )
 
 
def fee_collection_by_month():
    return run_query(
        """SELECT TO_CHAR(payment_date, 'Mon YYYY') AS month,
                  SUM(amount) AS collected
           FROM fee_payments
           GROUP BY TO_CHAR(payment_date, 'Mon YYYY'), DATE_TRUNC('month', payment_date)
           ORDER BY DATE_TRUNC('month', payment_date);"""
    )
 
 
def course_wise_students():
    return run_query(
        "SELECT course, COUNT(*) AS students FROM students GROUP BY course ORDER BY students DESC;"
    )
 
 
def gender_distribution():
    return run_query(
        "SELECT gender, COUNT(*) AS count FROM students GROUP BY gender;"
    )
 
 
def show():
    # ── Custom CSS ────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Page background */
    .main { background-color: #f0f4f8; }
 
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1976D2, #42a5f5);
        border-radius: 16px;
        padding: 24px 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(25,118,210,0.3);
        margin-bottom: 10px;
    }
    .kpi-card.green  { background: linear-gradient(135deg, #2e7d32, #66bb6a); box-shadow: 0 4px 15px rgba(46,125,50,0.3); }
    .kpi-card.orange { background: linear-gradient(135deg, #e65100, #ffa726); box-shadow: 0 4px 15px rgba(230,81,0,0.3); }
    .kpi-card.purple { background: linear-gradient(135deg, #6a1b9a, #ab47bc); box-shadow: 0 4px 15px rgba(106,27,154,0.3); }
 
    .kpi-number { font-size: 2.4rem; font-weight: 800; margin: 8px 0 4px 0; }
    .kpi-label  { font-size: 0.95rem; opacity: 0.92; font-weight: 500; letter-spacing: 0.5px; }
    .kpi-icon   { font-size: 1.8rem; margin-bottom: 4px; }
 
    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1565C0;
        margin: 18px 0 10px 0;
        padding-left: 10px;
        border-left: 4px solid #1976D2;
    }
 
    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(120deg, #0d47a1, #1976D2, #42a5f5);
        border-radius: 16px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 6px 20px rgba(13,71,161,0.35);
    }
    .welcome-banner h1 { font-size: 2rem; margin: 0; font-weight: 800; }
    .welcome-banner p  { font-size: 1rem; margin: 6px 0 0 0; opacity: 0.88; }
 
    /* Top student badge */
    .top-student {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-left: 4px solid #1976D2;
    }
    .rank-badge {
        background: #1976D2;
        color: white;
        border-radius: 50%;
        width: 28px; height: 28px;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)
 
    # ── Welcome Banner ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="welcome-banner">
        <h1>🏫 School ERP Dashboard</h1>
        <p>Welcome, Admin! Here's your school at a glance.</p>
    </div>
    """, unsafe_allow_html=True)
 
    # ── KPI Data ─────────────────────────────────────────────────────────────
    kpi = kpi_data()
    if not kpi:
        st.error("Could not load dashboard data. Check database connection.")
        return
 
    total_students  = int(kpi.get("total_students", 0))
    total_collected = float(kpi.get("total_collected", 0))
    total_present   = int(kpi.get("total_present", 0))
    total_classes   = int(kpi.get("total_classes", 1)) or 1
    att_pct         = round(100 * total_present / total_classes, 1)
    total_pending   = max(0, total_students * TOTAL_FEE_PER_STUDENT - int(total_collected))
 
    # ── KPI Cards ─────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">👨‍🎓</div>
            <div class="kpi-number">{total_students}</div>
            <div class="kpi-label">Total Students</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card green">
            <div class="kpi-icon">💰</div>
            <div class="kpi-number">₹{int(total_collected):,}</div>
            <div class="kpi-label">Fee Collected</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card orange">
            <div class="kpi-icon">⏳</div>
            <div class="kpi-number">₹{total_pending:,}</div>
            <div class="kpi-label">Fee Pending</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card purple">
            <div class="kpi-icon">📅</div>
            <div class="kpi-number">{att_pct}%</div>
            <div class="kpi-label">Avg Attendance</div>
        </div>""", unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # ── Row 2: Top Students + Attendance Chart ────────────────────────────────
    col_left, col_right = st.columns([1, 1.6])
 
    with col_left:
        st.markdown('<div class="section-header">🏆 Top Performing Students</div>', unsafe_allow_html=True)
        top = top_students()
        if top:
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
            for i, s in enumerate(top):
                pct = float(s["avg_percentage"])
                color = "#ffd700" if i == 0 else "#c0c0c0" if i == 1 else "#cd7f32" if i == 2 else "#1976D2"
                st.markdown(f"""
                <div class="top-student">
                    <span style="font-size:1.3rem">{medals[i]}</span>
                    <span style="font-weight:600; flex:1; margin-left:10px">{s['name']}</span>
                    <span style="background:{color}; color:white; padding:3px 10px;
                           border-radius:20px; font-weight:700; font-size:0.9rem">{pct}%</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No result data yet.")
 
    with col_right:
        st.markdown('<div class="section-header">📅 Attendance by Subject</div>', unsafe_allow_html=True)
        att = attendance_summary()
        if att:
            df_att = pd.DataFrame(att)
            fig = go.Figure(go.Bar(
                x=df_att["subject_name"],
                y=df_att["pct"],
                marker=dict(
                    color=df_att["pct"],
                    colorscale="Blues",
                    showscale=False,
                    line=dict(color="white", width=1.5)
                ),
                text=df_att["pct"].astype(str) + "%",
                textposition="outside",
            ))
            fig.add_hline(y=75, line_dash="dash", line_color="red",
                          annotation_text="75% minimum", annotation_position="top right")
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                yaxis=dict(range=[0, 110], showgrid=True, gridcolor="#f0f0f0"),
                xaxis=dict(tickangle=-20),
                font=dict(family="sans-serif"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No attendance data yet.")
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # ── Row 3: Fee Chart + Course Pie + Gender Pie ────────────────────────────
    col1, col2, col3 = st.columns(3)
 
    with col1:
        st.markdown('<div class="section-header">💳 Monthly Fee Collection</div>', unsafe_allow_html=True)
        monthly = fee_collection_by_month()
        if monthly:
            df_m = pd.DataFrame(monthly)
            fig2 = px.bar(df_m, x="month", y="collected",
                          color="collected",
                          color_continuous_scale="Teal",
                          text_auto=True)
            fig2.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside")
            fig2.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                coloraxis_showscale=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                yaxis_title="Amount (₹)",
                xaxis_title="",
                font=dict(family="sans-serif"),
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No fee data yet.")
 
    with col2:
        st.markdown('<div class="section-header">🎓 Students by Course</div>', unsafe_allow_html=True)
        course_data = course_wise_students()
        if course_data:
            df_c = pd.DataFrame(course_data)
            fig3 = px.pie(df_c, names="course", values="students",
                          color_discrete_sequence=px.colors.qualitative.Set2,
                          hole=0.45)
            fig3.update_traces(textposition="outside", textinfo="label+percent")
            fig3.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                showlegend=False,
                paper_bgcolor="white",
                font=dict(family="sans-serif"),
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No data yet.")
 
    with col3:
        st.markdown('<div class="section-header">👥 Gender Distribution</div>', unsafe_allow_html=True)
        gender = gender_distribution()
        if gender:
            df_g = pd.DataFrame(gender)
            fig4 = px.pie(df_g, names="gender", values="count",
                          color_discrete_map={"Male": "#1976D2", "Female": "#e91e8c", "Other": "#ff9800"},
                          hole=0.45)
            fig4.update_traces(textposition="outside", textinfo="label+value")
            fig4.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                showlegend=False,
                paper_bgcolor="white",
                font=dict(family="sans-serif"),
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No data yet.")
 
    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:#999; font-size:0.85rem; padding:10px 0">
        🏫 School ERP Mini System &nbsp;|&nbsp; Built with Python + Streamlit + PostgreSQL
    </div>
    """, unsafe_allow_html=True)