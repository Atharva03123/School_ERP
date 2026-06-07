import streamlit as st
import pandas as pd
from utils.db import run_query, execute
from utils.helpers import show_dataframe, success, error, page_header

MAX_MARKS = 100


def get_students():
    return run_query("SELECT student_id, name FROM students ORDER BY name;")


def get_subjects():
    return run_query("SELECT subject_id, subject_name FROM subjects ORDER BY subject_name;")


def upsert_marks(student_id, subject_id, exam_type, marks_obtained, max_marks=MAX_MARKS):
    return execute(
        """INSERT INTO results (student_id, subject_id, exam_type, marks_obtained, max_marks)
           VALUES (%s, %s, %s, %s, %s)
           ON CONFLICT (student_id, subject_id, exam_type)
           DO UPDATE SET marks_obtained = EXCLUDED.marks_obtained, max_marks = EXCLUDED.max_marks;""",
        (student_id, subject_id, exam_type, marks_obtained, max_marks),
    )


def get_results(student_id=None):
    where  = "WHERE r.student_id = %s" if student_id else ""
    params = (student_id,) if student_id else None
    return run_query(
        f"""SELECT s.name AS student, sub.subject_name AS subject, r.exam_type,
                   r.marks_obtained, r.max_marks,
                   ROUND(100.0 * r.marks_obtained / r.max_marks, 2) AS percentage
            FROM results r
            JOIN students s ON s.student_id = r.student_id
            JOIN subjects sub ON sub.subject_id = r.subject_id
            {where}
            ORDER BY s.name, sub.subject_name, r.exam_type;""",
        params,
    )


def get_student_report(student_id):
    """Aggregated result card for one student."""
    return run_query(
        """SELECT sub.subject_name,
                  MAX(CASE WHEN r.exam_type='Internal' THEN r.marks_obtained END) AS internal,
                  MAX(CASE WHEN r.exam_type='External' THEN r.marks_obtained END) AS external,
                  SUM(r.marks_obtained) AS total,
                  SUM(r.max_marks) AS max_total,
                  ROUND(100.0 * SUM(r.marks_obtained) / NULLIF(SUM(r.max_marks), 0), 2) AS percentage
           FROM results r
           JOIN subjects sub ON sub.subject_id = r.subject_id
           WHERE r.student_id = %s
           GROUP BY sub.subject_name
           ORDER BY sub.subject_name;""",
        (student_id,),
    )


def get_grade(pct):
    if pct >= 90: return "O (Outstanding)"
    if pct >= 75: return "A+"
    if pct >= 60: return "A"
    if pct >= 50: return "B"
    if pct >= 40: return "C"
    return "F (Fail)"


# ── UI ───────────────────────────────────────────────────────────────────────

def show():
    page_header("📝 Result Management", "Enter marks, calculate results and generate report cards")

    tab1, tab2, tab3 = st.tabs(["📥 Enter Marks", "📋 View Results", "🎓 Report Card"])

    students = get_students()
    subjects = get_subjects()

    if not students or not subjects:
        st.warning("Please ensure students and subjects are available in the database.")
        return

    stu_map = {s["name"]: s["student_id"] for s in students}
    sub_map = {s["subject_name"]: s["subject_id"] for s in subjects}

    # ── Enter Marks ──────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Enter / Update Marks")
        with st.form("marks_form"):
            c1, c2, c3 = st.columns(3)
            sel_stu    = c1.selectbox("Student", list(stu_map.keys()))
            sel_sub    = c2.selectbox("Subject", list(sub_map.keys()))
            exam_type  = c3.selectbox("Exam Type", ["Internal", "External", "Practical"])
            max_marks  = c1.number_input("Max Marks", value=100, min_value=10, max_value=500, step=10)
            obtained   = c2.number_input("Marks Obtained", value=0, min_value=0, max_value=int(max_marks))
            submitted  = st.form_submit_button("Save Marks", use_container_width=True)

        if submitted:
            if obtained > max_marks:
                error("Marks obtained cannot exceed max marks.")
            else:
                if upsert_marks(stu_map[sel_stu], sub_map[sel_sub], exam_type, obtained, max_marks):
                    pct = round(100 * obtained / max_marks, 2)
                    success(f"Marks saved! {sel_stu} – {sel_sub}: {obtained}/{max_marks} ({pct}%) → {get_grade(pct)}")
                else:
                    error("Failed to save marks.")

    # ── View Results ─────────────────────────────────────────────────────────
    with tab2:
        st.subheader("All Results")
        f_stu = st.selectbox("Filter by Student", ["All"] + list(stu_map.keys()), key="r_stu")
        sid   = stu_map[f_stu] if f_stu != "All" else None
        results = get_results(sid)
        show_dataframe(results)
        if results:
            df = pd.DataFrame(results)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode(), "results.csv", "text/csv")

    # ── Report Card ──────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Student Report Card")
        sel_stu = st.selectbox("Select Student", list(stu_map.keys()), key="rc_stu")
        sid = stu_map[sel_stu]
        report = get_student_report(sid)

        if not report:
            st.info("No results found for this student.")
        else:
            df = pd.DataFrame(report)

            overall_total = df["total"].sum()
            overall_max   = df["max_total"].sum()
            overall_pct   = round(100 * overall_total / overall_max, 2) if overall_max else 0
            grade = get_grade(overall_pct)
            result_status = "PASS ✅" if overall_pct >= 40 else "FAIL ❌"

            st.markdown(f"### 📄 Report Card — {sel_stu}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Overall %", f"{overall_pct}%")
            c2.metric("Grade", grade)
            c3.metric("Result", result_status)

            st.divider()
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode()
            st.download_button("⬇️ Download Report Card", csv,
                               f"report_card_{sel_stu.replace(' ', '_')}.csv", "text/csv")
