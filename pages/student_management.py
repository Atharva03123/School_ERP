import streamlit as st
import pandas as pd
from utils.db import run_query, execute
from utils.helpers import show_dataframe, success, error, page_header

# ── helpers ──────────────────────────────────────────────────────────────────

def get_all_students():
    return run_query("SELECT * FROM students ORDER BY student_id;")


def get_student_by_id(sid):
    rows = run_query("SELECT * FROM students WHERE student_id = %s;", (sid,))
    return rows[0] if rows else None


def add_student(name, dob, gender, course, year, email, phone, address):
    return execute(
        """INSERT INTO students (name, dob, gender, course, year, email, phone, address)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
        (name, dob, gender, course, year, email, phone, address),
    )


def update_student(sid, name, dob, gender, course, year, email, phone, address):
    return execute(
        """UPDATE students SET name=%s, dob=%s, gender=%s, course=%s, year=%s,
           email=%s, phone=%s, address=%s WHERE student_id=%s;""",
        (name, dob, gender, course, year, email, phone, address, sid),
    )


def delete_student(sid):
    return execute("DELETE FROM students WHERE student_id = %s;", (sid,))


# ── UI ───────────────────────────────────────────────────────────────────────

def show():
    page_header("👨‍🎓 Student Management", "Add, update, delete and view student records")

    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Student", "✏️ Update Student",
                                       "🗑️ Delete Student", "📋 View Students"])

    # ── Add ──────────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Add New Student")
        with st.form("add_student_form"):
            c1, c2 = st.columns(2)
            name    = c1.text_input("Full Name *")
            dob     = c2.date_input("Date of Birth")
            gender  = c1.selectbox("Gender", ["Male", "Female", "Other"])
            course  = c2.selectbox("Course", ["B.Sc CS", "B.Sc IT", "BCA", "B.Com", "BA"])
            year    = c1.selectbox("Year", [1, 2, 3])
            email   = c2.text_input("Email")
            phone   = c1.text_input("Phone")
            address = st.text_area("Address")
            submitted = st.form_submit_button("Add Student", use_container_width=True)

        if submitted:
            if not name.strip():
                error("Student name is required.")
            else:
                if add_student(name, dob, gender, course, year, email, phone, address):
                    success(f"Student '{name}' added successfully!")
                else:
                    error("Failed to add student.")

    # ── Update ───────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("Update Student Details")
        students = get_all_students()
        if not students:
            st.info("No students in the database yet.")
        else:
            options = {f"{s['student_id']} – {s['name']}": s['student_id'] for s in students}
            chosen_label = st.selectbox("Select Student", list(options.keys()), key="upd_sel")
            sid = options[chosen_label]
            s = get_student_by_id(sid)
            if s:
                with st.form("update_form"):
                    c1, c2 = st.columns(2)
                    name    = c1.text_input("Full Name", value=s["name"])
                    dob     = c2.date_input("Date of Birth", value=s["dob"])
                    gender  = c1.selectbox("Gender", ["Male", "Female", "Other"],
                                           index=["Male", "Female", "Other"].index(s["gender"]))
                    courses = ["B.Sc CS", "B.Sc IT", "BCA", "B.Com", "BA"]
                    course  = c2.selectbox("Course", courses,
                                           index=courses.index(s["course"]) if s["course"] in courses else 0)
                    year    = c1.selectbox("Year", [1, 2, 3], index=s["year"] - 1)
                    email   = c2.text_input("Email", value=s["email"] or "")
                    phone   = c1.text_input("Phone", value=s["phone"] or "")
                    address = st.text_area("Address", value=s["address"] or "")
                    upd_btn = st.form_submit_button("Update Student", use_container_width=True)

                if upd_btn:
                    if update_student(sid, name, dob, gender, course, year, email, phone, address):
                        success("Student updated successfully!")
                    else:
                        error("Update failed.")

    # ── Delete ───────────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Delete Student")
        students = get_all_students()
        if not students:
            st.info("No students available.")
        else:
            options = {f"{s['student_id']} – {s['name']}": s['student_id'] for s in students}
            chosen_label = st.selectbox("Select Student to Delete", list(options.keys()), key="del_sel")
            sid = options[chosen_label]
            st.warning("⚠️ Deleting a student removes all related attendance, fee, and result records.")
            if st.button("🗑️ Confirm Delete", type="primary"):
                if delete_student(sid):
                    success("Student deleted.")
                    st.rerun()
                else:
                    error("Deletion failed.")

    # ── View ─────────────────────────────────────────────────────────────────
    with tab4:
        st.subheader("All Students")
        students = get_all_students()
        show_dataframe(students)
        if students:
            df = pd.DataFrame(students)
            csv = df.to_csv(index=False).encode()
            st.download_button("⬇️ Download CSV", csv, "students.csv", "text/csv")
