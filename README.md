# 🏫 School ERP Mini System

A beginner-to-intermediate level School ERP (Enterprise Resource Planning) system built
with **Python**, **PostgreSQL**, **Streamlit**, and **Pandas** — ideal for a B.Sc Computer
Science fresher project.

---

## 📌 Project Overview

This project simulates a simple school management system that allows administrators to:

- Manage student records
- Track attendance subject-wise
- Record and monitor fee payments
- Enter exam marks and generate report cards
- View a consolidated admin dashboard

It is intentionally kept **simple and clean**, avoiding enterprise features like payroll,
SMS gateways, AI modules, multi-school support, or complex role-based authentication.

---

## 📁 Folder Structure

```
school_erp/
│
├── app.py                      # Main Streamlit entry point
├── schema.sql                  # Database schema + sample data
├── requirements.txt            # Python dependencies
├── .gitignore
│
├── pages/
│   ├── __init__.py
│   ├── dashboard.py            # Admin Dashboard
│   ├── student_management.py   # Student CRUD
│   ├── attendance_management.py# Attendance module
│   ├── fee_management.py       # Fee module
│   └── result_management.py    # Results / marks module
│
├── utils/
│   ├── __init__.py
│   ├── db.py                   # PostgreSQL connection helpers
│   └── helpers.py              # Shared UI helper functions
│
└── .streamlit/
    ├── config.toml             # Theme and server settings
    └── secrets.toml.example    # DB credentials template
```

---

## 🗄️ Database Schema

| Table          | Description                          | Key Columns                              |
|---------------|--------------------------------------|------------------------------------------|
| `students`    | Core student records                 | student_id (PK), name, course, year      |
| `subjects`    | Subject master list                  | subject_id (PK), subject_name, course    |
| `attendance`  | Daily attendance per subject         | FK → students, subjects; UNIQUE per day  |
| `fee_payments`| Fee transaction records              | FK → students; amount, payment_mode      |
| `results`     | Exam marks per subject & exam type   | FK → students, subjects; exam_type       |

All child tables reference `students` with **ON DELETE CASCADE** — deleting a student
removes their attendance, fee, and result records automatically.

---

## ⚙️ Installation Steps

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- pip

### Step 1 – Clone / Download the project
```bash
git clone https://github.com/your-username/school_erp.git
cd school_erp
```

### Step 2 – Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### Step 3 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 – Set up PostgreSQL
```sql
-- Run in psql as superuser
CREATE DATABASE school_erp;
CREATE USER erp_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE school_erp TO erp_user;
```

### Step 5 – Load the schema and sample data
```bash
psql -U erp_user -d school_erp -f schema.sql
```

### Step 6 – Configure database credentials
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and fill in your DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
```

### Step 7 – Run the app
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501**

---

## 🧩 Modules

### 1. 🏠 Admin Dashboard
- Total students count
- Total fee collected vs pending
- Overall attendance percentage
- Top 5 performing students
- Fee collection bar chart by month
- Students by course distribution chart

### 2. 👨‍🎓 Student Management
- Add new student with all details
- Update existing student information
- Delete student (cascades to all related records)
- View all students with export to CSV

### 3. 📅 Attendance Management
- Mark individual attendance (Present / Absent)
- Bulk mark attendance for all students in one subject
- Upsert logic – re-marking the same day updates, not duplicates
- View attendance records with filters
- Attendance percentage report (rows < 75% highlighted red)

### 4. 💰 Fee Management
- Record fee payments with mode (Cash, Online, Cheque, DD)
- View pending fees per student (based on ₹50,000 annual fee)
- Fee summary with total collected / pending metrics
- Filter payments by student; export to CSV

### 5. 📝 Result Management
- Enter / update marks per student, subject, and exam type
- Supports Internal, External, Practical exams
- Auto-calculates percentage and grade (O, A+, A, B, C, F)
- Individual student report card with overall percentage and pass/fail
- Export report card to CSV

---

## 🔮 Future Improvements

| Idea                          | Difficulty  |
|-------------------------------|-------------|
| Login page (admin password)   | Easy        |
| Student photo upload          | Medium      |
| Email fee receipt (smtplib)   | Medium      |
| Timetable management          | Medium      |
| Export report card to PDF     | Medium      |
| Library book tracking module  | Medium      |
| Multi-teacher / subject mapping| Hard       |
| Deploy on Streamlit Cloud     | Easy        |
| REST API with FastAPI         | Hard        |

---

## 🛠️ Tech Stack

| Technology   | Role                            |
|--------------|---------------------------------|
| Python 3.9+  | Core language                   |
| Streamlit    | Web UI framework                |
| PostgreSQL   | Relational database             |
| psycopg2     | PostgreSQL adapter for Python   |
| Pandas       | Data manipulation & CSV export  |

---

## 📄 License

This project is free to use for educational purposes.

---

*Built as a B.Sc Computer Science fresher project.*
