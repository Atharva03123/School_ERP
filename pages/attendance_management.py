import streamlit as st
import pandas as pd
from datetime import date
from utils.db import run_query, execute
from utils.helpers import show_dataframe, success, error, page_header


def get_students():
    return run_query("SELECT student_id, name FROM students ORDER BY name;")


def get_subjects():
    return run_query("SELECT subject_id, subject_name FROM subjects ORDER BY subject_name;")


def mark_attendance(student_id, subject_id, att_date, status):
    # upsert – avoids duplicate entries for the same day/subject/student
    return execute(
        """INSERT INTO attendance (student_id, subject_id, date, status)
           VALUES (%s, %s, %s, %s)
           ON CONFLICT (student_id, subject_id, date) DO UPDATE SET status = EXCLUDED.status;""",
        (student_id, subject_id, att_date, status),
    )


def get_attendance(student_id=None, subject_id=None):
    where, params = [], []
    if student_id:
        where.append("a.student_id = %s"); params.append(student_id)
    if subject_id:
        where.append("a.subject_id = %s"); params.append(subject_id)
    clause = "WHERE " + " AND ".join(where) if where else ""
    return run_query(
        f"""SELECT s.name AS student, sub.subject_name AS subject,
                   a.date, a.status
            FROM attendance a
            JOIN students s ON s.student_id = a.student_id
            JOIN subjects sub ON sub.subject_id = a.subject_id
            {clause}
            ORDER BY a.date DESC;""",
        params or None,
    )


def get_percentage_report():
    return run_query(
        """SELECT s.name AS student, sub.subject_name AS subject,
                  COUNT(*) AS total_classes,
                  SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present,
                  ROUND(
                      100.0 * SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(*), 2
                  ) AS percentage
           FROM attendance a
           JOIN students s ON s.student_id = a.student_id
           JOIN subjects sub ON sub.subject_id = a.subject_id
           GROUP BY s.name, sub.subject_name
           ORDER BY s.name, sub.subject_name;"""
    )


# ── UI ───────────────────────────────────────────────────────────────────────

def show():
    page_header("📅 Attendance Management", "Mark and track student attendance")

    tab1, tab2, tab3 = st.tabs(["✅ Mark Attendance", "📋 View Records", "📊 Percentage Report"])

    students = get_students()
    subjects = get_subjects()

    if not students:
        st.warning("No students found. Please add students first.")
        return
    if not subjects:
        st.warning("No subjects found. Please seed the database with sample data.")
        return

    stu_map = {s["name"]: s["student_id"] for s in students}
    sub_map = {s["subject_name"]: s["subject_id"] for s in subjects}

    # ── Mark ─────────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Mark Attendance")
        c1, c2, c3 = st.columns(3)
        sel_stu  = c1.selectbox("Student", list(stu_map.keys()))
        sel_sub  = c2.selectbox("Subject", list(sub_map.keys()))
        att_date = c3.date_input("Date", value=date.today())
        status   = st.radio("Status", ["Present", "Absent"], horizontal=True)

        if st.button("Mark Attendance", type="primary"):
            if mark_attendance(stu_map[sel_stu], sub_map[sel_sub], att_date, status):
                success(f"Attendance marked: {sel_stu} – {status} on {att_date}")
            else:
                error("Failed to mark attendance.")

        st.divider()
        st.subheader("Bulk Mark for a Date")
        st.caption("Quickly mark all students for one subject on one day.")
        bulk_sub  = st.selectbox("Subject (bulk)", list(sub_map.keys()), key="bulk_sub")
        bulk_date = st.date_input("Date (bulk)", value=date.today(), key="bulk_date")
        statuses = {}
        for stu in students:
            statuses[stu["student_id"]] = st.radio(
                stu["name"], ["Present", "Absent"], horizontal=True,
                key=f"bulk_{stu['student_id']}"
            )
        if st.button("Save Bulk Attendance", type="primary"):
            ok = True
            for sid, stat in statuses.items():
                if not mark_attendance(sid, sub_map[bulk_sub], bulk_date, stat):
                    ok = False
            success("Bulk attendance saved!") if ok else error("Some records failed.")

    # ── View ─────────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("View Attendance Records")
        c1, c2 = st.columns(2)
        f_stu = c1.selectbox("Filter by Student", ["All"] + list(stu_map.keys()), key="v_stu")
        f_sub = c2.selectbox("Filter by Subject", ["All"] + list(sub_map.keys()), key="v_sub")

        sid = stu_map[f_stu] if f_stu != "All" else None
        suid = sub_map[f_sub] if f_sub != "All" else None
        records = get_attendance(sid, suid)
        show_dataframe(records)

    # ── Percentage ───────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Attendance Percentage Report")
        report = get_percentage_report()
        if not report:
            st.info("No attendance data available yet.")
        else:
            df = pd.DataFrame(report)
            # colour code: <75% red
            def highlight(row):
                color = "background-color: #ffcccc" if row["percentage"] < 75 else ""
                return [color] * len(row)
            st.dataframe(df.style.apply(highlight, axis=1), use_container_width=True)
            csv = df.to_csv(index=False).encode()
            st.download_button("⬇️ Download Report", csv, "attendance_report.csv", "text/csv")
