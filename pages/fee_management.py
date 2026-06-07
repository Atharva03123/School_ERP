import streamlit as st
import pandas as pd
from datetime import date
from utils.db import run_query, execute
from utils.helpers import show_dataframe, success, error, page_header

TOTAL_FEE = 50000  # annual fee per student (INR)


def get_students():
    return run_query("SELECT student_id, name FROM students ORDER BY name;")


def record_payment(student_id, amount, payment_date, payment_mode, remarks):
    return execute(
        """INSERT INTO fee_payments (student_id, amount, payment_date, payment_mode, remarks)
           VALUES (%s, %s, %s, %s, %s);""",
        (student_id, amount, payment_date, payment_mode, remarks),
    )


def get_payments(student_id=None):
    where  = "WHERE fp.student_id = %s" if student_id else ""
    params = (student_id,) if student_id else None
    return run_query(
        f"""SELECT s.name AS student, fp.amount, fp.payment_date,
                   fp.payment_mode, fp.remarks, fp.payment_id
            FROM fee_payments fp
            JOIN students s ON s.student_id = fp.student_id
            {where}
            ORDER BY fp.payment_date DESC;""",
        params,
    )


def get_fee_summary():
    return run_query(
        f"""SELECT s.name AS student, s.course, s.year,
                   COALESCE(SUM(fp.amount), 0) AS paid,
                   {TOTAL_FEE} - COALESCE(SUM(fp.amount), 0) AS pending
            FROM students s
            LEFT JOIN fee_payments fp ON fp.student_id = s.student_id
            GROUP BY s.student_id, s.name, s.course, s.year
            ORDER BY pending DESC;"""
    )


# ── UI ───────────────────────────────────────────────────────────────────────

def show():
    page_header("💰 Fee Management", "Record payments, track dues and generate summaries")

    tab1, tab2, tab3 = st.tabs(["💳 Record Payment", "⏳ Pending Fees", "📊 Fee Summary"])

    students = get_students()
    if not students:
        st.warning("No students found. Please add students first.")
        return

    stu_map = {s["name"]: s["student_id"] for s in students}

    # ── Record ───────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Record Fee Payment")
        with st.form("fee_form"):
            c1, c2 = st.columns(2)
            sel_stu      = c1.selectbox("Student", list(stu_map.keys()))
            amount       = c2.number_input("Amount (₹)", min_value=100, max_value=200000, step=500, value=10000)
            payment_date = c1.date_input("Payment Date", value=date.today())
            payment_mode = c2.selectbox("Payment Mode", ["Cash", "Online Transfer", "Cheque", "DD"])
            remarks      = st.text_input("Remarks (optional)")
            submitted    = st.form_submit_button("Record Payment", use_container_width=True)

        if submitted:
            if record_payment(stu_map[sel_stu], amount, payment_date, payment_mode, remarks):
                success(f"Payment of ₹{amount:,} recorded for {sel_stu}.")
            else:
                error("Failed to record payment.")

    # ── Pending ──────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("Students with Pending Fees")
        summary = get_fee_summary()
        pending = [r for r in summary if r["pending"] > 0]
        if not pending:
            st.success("🎉 All students have cleared their fees!")
        else:
            df = pd.DataFrame(pending)
            st.dataframe(df, use_container_width=True)
            total_pending = sum(r["pending"] for r in pending)
            st.metric("Total Pending (₹)", f"₹{total_pending:,}")

    # ── Summary ──────────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Complete Fee Summary")
        f_stu = st.selectbox("Filter by Student (optional)", ["All"] + list(stu_map.keys()))
        sid = stu_map[f_stu] if f_stu != "All" else None
        payments = get_payments(sid)

        col1, col2, col3 = st.columns(3)
        total_collected = sum(p["amount"] for p in payments)
        col1.metric("Total Collected (₹)", f"₹{total_collected:,}")

        summary = get_fee_summary()
        total_pending = sum(r["pending"] for r in summary)
        col2.metric("Total Pending (₹)", f"₹{total_pending:,}")
        col3.metric("Total Students", len(students))

        show_dataframe(payments, "Payment Records")
        if payments:
            df = pd.DataFrame(payments)
            csv = df.to_csv(index=False).encode()
            st.download_button("⬇️ Download CSV", csv, "fee_payments.csv", "text/csv")
