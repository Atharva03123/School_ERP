-- ============================================================
--  School ERP Mini System – Database Schema
--  Compatible with PostgreSQL 13+
-- ============================================================

-- Drop existing tables (cascade removes dependent objects)
DROP TABLE IF EXISTS results      CASCADE;
DROP TABLE IF EXISTS fee_payments CASCADE;
DROP TABLE IF EXISTS attendance   CASCADE;
DROP TABLE IF EXISTS subjects     CASCADE;
DROP TABLE IF EXISTS students     CASCADE;

-- ────────────────────────────────────────────────────────────
--  1. Students
-- ────────────────────────────────────────────────────────────
CREATE TABLE students (
    student_id  SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    dob         DATE,
    gender      VARCHAR(10)  CHECK (gender IN ('Male', 'Female', 'Other')),
    course      VARCHAR(50),
    year        INTEGER      CHECK (year BETWEEN 1 AND 3),
    email       VARCHAR(100),
    phone       VARCHAR(15),
    address     TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ────────────────────────────────────────────────────────────
--  2. Subjects
-- ────────────────────────────────────────────────────────────
CREATE TABLE subjects (
    subject_id   SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL UNIQUE,
    course       VARCHAR(50),
    year         INTEGER
);

-- ────────────────────────────────────────────────────────────
--  3. Attendance
-- ────────────────────────────────────────────────────────────
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id    INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id    INTEGER REFERENCES subjects(subject_id) ON DELETE CASCADE,
    date          DATE    NOT NULL,
    status        VARCHAR(10) CHECK (status IN ('Present', 'Absent')) DEFAULT 'Present',
    UNIQUE (student_id, subject_id, date)   -- prevent duplicate entries
);

-- ────────────────────────────────────────────────────────────
--  4. Fee Payments
-- ────────────────────────────────────────────────────────────
CREATE TABLE fee_payments (
    payment_id   SERIAL PRIMARY KEY,
    student_id   INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
    amount       NUMERIC(10,2) NOT NULL CHECK (amount > 0),
    payment_date DATE          NOT NULL DEFAULT CURRENT_DATE,
    payment_mode VARCHAR(30)   CHECK (payment_mode IN ('Cash','Online Transfer','Cheque','DD')),
    remarks      TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ────────────────────────────────────────────────────────────
--  5. Results / Marks
-- ────────────────────────────────────────────────────────────
CREATE TABLE results (
    result_id      SERIAL PRIMARY KEY,
    student_id     INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id     INTEGER REFERENCES subjects(subject_id) ON DELETE CASCADE,
    exam_type      VARCHAR(20) CHECK (exam_type IN ('Internal','External','Practical')),
    marks_obtained NUMERIC(6,2) NOT NULL,
    max_marks      NUMERIC(6,2) NOT NULL DEFAULT 100,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (student_id, subject_id, exam_type)
);

-- ============================================================
--  INDEXES  (improve query performance)
-- ============================================================
CREATE INDEX idx_attendance_student  ON attendance(student_id);
CREATE INDEX idx_attendance_date     ON attendance(date);
CREATE INDEX idx_fee_student         ON fee_payments(student_id);
CREATE INDEX idx_results_student     ON results(student_id);

-- ============================================================
--  SAMPLE DATA
-- ============================================================

-- Subjects
INSERT INTO subjects (subject_name, course, year) VALUES
    ('Python Programming',      'B.Sc CS', 1),
    ('Data Structures',         'B.Sc CS', 1),
    ('Database Management',     'B.Sc CS', 2),
    ('Operating Systems',       'B.Sc CS', 2),
    ('Computer Networks',       'B.Sc CS', 3),
    ('Software Engineering',    'B.Sc CS', 3),
    ('Mathematics',             'B.Sc CS', 1),
    ('Web Technologies',        'B.Sc CS', 2);

-- Students
INSERT INTO students (name, dob, gender, course, year, email, phone, address) VALUES
    ('Aarav Sharma',   '2003-05-14', 'Male',   'B.Sc CS', 1, 'aarav@example.com',   '9876543210', 'Pune, Maharashtra'),
    ('Priya Patel',    '2003-08-22', 'Female', 'B.Sc CS', 1, 'priya@example.com',   '9876543211', 'Mumbai, Maharashtra'),
    ('Rohan Mehta',    '2002-11-30', 'Male',   'B.Sc CS', 2, 'rohan@example.com',   '9876543212', 'Nashik, Maharashtra'),
    ('Ananya Singh',   '2002-03-17', 'Female', 'B.Sc CS', 2, 'ananya@example.com',  '9876543213', 'Nagpur, Maharashtra'),
    ('Karan Joshi',    '2001-07-09', 'Male',   'B.Sc CS', 3, 'karan@example.com',   '9876543214', 'Aurangabad, Maharashtra'),
    ('Sneha Reddy',    '2001-12-25', 'Female', 'B.Sc CS', 3, 'sneha@example.com',   '9876543215', 'Hyderabad, Telangana'),
    ('Arjun Nair',     '2003-02-14', 'Male',   'BCA',     1, 'arjun@example.com',   '9876543216', 'Kochi, Kerala'),
    ('Divya Iyer',     '2002-06-03', 'Female', 'BCA',     2, 'divya@example.com',   '9876543217', 'Chennai, Tamil Nadu'),
    ('Vikram Gupta',   '2001-09-19', 'Male',   'B.Com',   3, 'vikram@example.com',  '9876543218', 'Delhi'),
    ('Pooja Desai',    '2003-01-11', 'Female', 'B.Sc IT', 1, 'pooja@example.com',   '9876543219', 'Surat, Gujarat');

-- Attendance (sample rows for last 5 days)
INSERT INTO attendance (student_id, subject_id, date, status) VALUES
    (1, 1, CURRENT_DATE - 4, 'Present'), (1, 1, CURRENT_DATE - 3, 'Present'),
    (1, 1, CURRENT_DATE - 2, 'Absent'),  (1, 1, CURRENT_DATE - 1, 'Present'),
    (1, 1, CURRENT_DATE,     'Present'),
    (2, 1, CURRENT_DATE - 4, 'Present'), (2, 1, CURRENT_DATE - 3, 'Absent'),
    (2, 1, CURRENT_DATE - 2, 'Present'), (2, 1, CURRENT_DATE - 1, 'Present'),
    (2, 1, CURRENT_DATE,     'Present'),
    (3, 3, CURRENT_DATE - 4, 'Absent'),  (3, 3, CURRENT_DATE - 3, 'Absent'),
    (3, 3, CURRENT_DATE - 2, 'Present'), (3, 3, CURRENT_DATE - 1, 'Present'),
    (3, 3, CURRENT_DATE,     'Present'),
    (4, 3, CURRENT_DATE - 4, 'Present'), (4, 3, CURRENT_DATE - 3, 'Present'),
    (4, 3, CURRENT_DATE - 2, 'Present'), (4, 3, CURRENT_DATE - 1, 'Absent'),
    (4, 3, CURRENT_DATE,     'Present'),
    (5, 5, CURRENT_DATE - 4, 'Present'), (5, 5, CURRENT_DATE - 3, 'Present'),
    (5, 5, CURRENT_DATE - 2, 'Present'), (5, 5, CURRENT_DATE - 1, 'Present'),
    (5, 5, CURRENT_DATE,     'Absent');

-- Fee Payments
INSERT INTO fee_payments (student_id, amount, payment_date, payment_mode, remarks) VALUES
    (1, 25000, CURRENT_DATE - 90, 'Cash',            'First instalment'),
    (1, 25000, CURRENT_DATE - 30, 'Online Transfer',  'Second instalment'),
    (2, 50000, CURRENT_DATE - 60, 'Cheque',           'Full year fee'),
    (3, 20000, CURRENT_DATE - 45, 'Cash',             'Partial payment'),
    (4, 50000, CURRENT_DATE - 15, 'Online Transfer',  'Full year fee'),
    (5, 30000, CURRENT_DATE - 5,  'Cash',             'Partial payment'),
    (6, 50000, CURRENT_DATE - 10, 'DD',               'Full year fee'),
    (7, 15000, CURRENT_DATE - 20, 'Cash',             'First instalment'),
    (8, 50000, CURRENT_DATE - 25, 'Online Transfer',  'Full year fee'),
    (9, 25000, CURRENT_DATE - 35, 'Cheque',           'Half year');

-- Results / Marks
INSERT INTO results (student_id, subject_id, exam_type, marks_obtained, max_marks) VALUES
    -- Student 1
    (1, 1, 'Internal', 38, 50), (1, 1, 'External', 72, 100),
    (1, 2, 'Internal', 42, 50), (1, 2, 'External', 68, 100),
    -- Student 2
    (2, 1, 'Internal', 45, 50), (2, 1, 'External', 88, 100),
    (2, 2, 'Internal', 47, 50), (2, 2, 'External', 91, 100),
    -- Student 3
    (3, 3, 'Internal', 30, 50), (3, 3, 'External', 55, 100),
    (3, 4, 'Internal', 32, 50), (3, 4, 'External', 60, 100),
    -- Student 4
    (4, 3, 'Internal', 44, 50), (4, 3, 'External', 82, 100),
    (4, 4, 'Internal', 40, 50), (4, 4, 'External', 78, 100),
    -- Student 5
    (5, 5, 'Internal', 48, 50), (5, 5, 'External', 92, 100),
    (5, 6, 'Internal', 46, 50), (5, 6, 'External', 89, 100),
    -- Student 6
    (6, 5, 'Internal', 35, 50), (6, 5, 'External', 65, 100),
    (6, 6, 'Internal', 38, 50), (6, 6, 'External', 70, 100);

-- Verify
SELECT 'students'    AS tbl, COUNT(*) FROM students
UNION ALL
SELECT 'subjects',   COUNT(*) FROM subjects
UNION ALL
SELECT 'attendance', COUNT(*) FROM attendance
UNION ALL
SELECT 'fee_payments', COUNT(*) FROM fee_payments
UNION ALL
SELECT 'results',    COUNT(*) FROM results;
