-- ============================================================
--  100 Students Sample Data — School ERP
--  Run this AFTER schema.sql
-- ============================================================

-- Clear existing data first
TRUNCATE TABLE results, fee_payments, attendance, students RESTART IDENTITY CASCADE;

-- ── 100 Students ─────────────────────────────────────────────
INSERT INTO students (name, dob, gender, course, year, email, phone, address) VALUES
('Aarav Sharma',      '2003-05-14', 'Male',   'B.Sc CS', 1, 'aarav.sharma@email.com',      '9876543001', 'Pune, Maharashtra'),
('Priya Patel',       '2003-08-22', 'Female', 'B.Sc CS', 1, 'priya.patel@email.com',       '9876543002', 'Mumbai, Maharashtra'),
('Rohan Mehta',       '2002-11-30', 'Male',   'B.Sc CS', 2, 'rohan.mehta@email.com',       '9876543003', 'Nashik, Maharashtra'),
('Ananya Singh',      '2002-03-17', 'Female', 'B.Sc CS', 2, 'ananya.singh@email.com',      '9876543004', 'Nagpur, Maharashtra'),
('Karan Joshi',       '2001-07-09', 'Male',   'B.Sc CS', 3, 'karan.joshi@email.com',       '9876543005', 'Aurangabad, Maharashtra'),
('Sneha Reddy',       '2001-12-25', 'Female', 'B.Sc CS', 3, 'sneha.reddy@email.com',       '9876543006', 'Hyderabad, Telangana'),
('Arjun Nair',        '2003-02-14', 'Male',   'BCA',     1, 'arjun.nair@email.com',        '9876543007', 'Kochi, Kerala'),
('Divya Iyer',        '2002-06-03', 'Female', 'BCA',     2, 'divya.iyer@email.com',        '9876543008', 'Chennai, Tamil Nadu'),
('Vikram Gupta',      '2001-09-19', 'Male',   'B.Com',   3, 'vikram.gupta@email.com',      '9876543009', 'Delhi'),
('Pooja Desai',       '2003-01-11', 'Female', 'B.Sc IT', 1, 'pooja.desai@email.com',       '9876543010', 'Surat, Gujarat'),
('Amit Kumar',        '2003-04-20', 'Male',   'B.Sc CS', 1, 'amit.kumar@email.com',        '9876543011', 'Patna, Bihar'),
('Riya Sharma',       '2003-07-15', 'Female', 'B.Sc CS', 1, 'riya.sharma@email.com',       '9876543012', 'Jaipur, Rajasthan'),
('Siddharth Rao',     '2002-09-28', 'Male',   'B.Sc CS', 2, 'siddharth.rao@email.com',     '9876543013', 'Bengaluru, Karnataka'),
('Kavya Menon',       '2002-12-05', 'Female', 'B.Sc CS', 2, 'kavya.menon@email.com',       '9876543014', 'Thiruvananthapuram, Kerala'),
('Nikhil Verma',      '2001-03-22', 'Male',   'B.Sc CS', 3, 'nikhil.verma@email.com',      '9876543015', 'Lucknow, UP'),
('Tanvi Joshi',       '2001-06-18', 'Female', 'B.Sc CS', 3, 'tanvi.joshi@email.com',       '9876543016', 'Ahmedabad, Gujarat'),
('Rahul Mishra',      '2003-10-07', 'Male',   'BCA',     1, 'rahul.mishra@email.com',      '9876543017', 'Bhopal, MP'),
('Shruti Das',        '2002-04-14', 'Female', 'BCA',     2, 'shruti.das@email.com',        '9876543018', 'Kolkata, WB'),
('Aditya Pandey',     '2001-08-30', 'Male',   'B.Com',   3, 'aditya.pandey@email.com',     '9876543019', 'Varanasi, UP'),
('Meera Nair',        '2003-02-25', 'Female', 'B.Sc IT', 1, 'meera.nair@email.com',        '9876543020', 'Kozhikode, Kerala'),
('Harsh Agarwal',     '2003-06-12', 'Male',   'B.Sc CS', 1, 'harsh.agarwal@email.com',     '9876543021', 'Agra, UP'),
('Ishita Bose',       '2003-09-03', 'Female', 'B.Sc CS', 1, 'ishita.bose@email.com',       '9876543022', 'Howrah, WB'),
('Pranav Kulkarni',   '2002-01-19', 'Male',   'B.Sc CS', 2, 'pranav.kulkarni@email.com',   '9876543023', 'Pune, Maharashtra'),
('Nandini Pillai',    '2002-05-08', 'Female', 'B.Sc CS', 2, 'nandini.pillai@email.com',    '9876543024', 'Ernakulam, Kerala'),
('Yash Tiwari',       '2001-11-27', 'Male',   'B.Sc CS', 3, 'yash.tiwari@email.com',       '9876543025', 'Kanpur, UP'),
('Simran Kaur',       '2001-04-16', 'Female', 'B.Sc CS', 3, 'simran.kaur@email.com',       '9876543026', 'Amritsar, Punjab'),
('Dev Chauhan',       '2003-08-09', 'Male',   'BCA',     1, 'dev.chauhan@email.com',       '9876543027', 'Indore, MP'),
('Pallavi Shukla',    '2002-03-01', 'Female', 'BCA',     2, 'pallavi.shukla@email.com',    '9876543028', 'Allahabad, UP'),
('Manish Yadav',      '2001-07-23', 'Male',   'B.Com',   3, 'manish.yadav@email.com',      '9876543029', 'Ranchi, Jharkhand'),
('Ankita Ghosh',      '2003-11-14', 'Female', 'B.Sc IT', 1, 'ankita.ghosh@email.com',      '9876543030', 'Durgapur, WB'),
('Suraj Patil',       '2003-03-28', 'Male',   'B.Sc CS', 1, 'suraj.patil@email.com',       '9876543031', 'Solapur, Maharashtra'),
('Deepika Raj',       '2003-06-17', 'Female', 'B.Sc CS', 1, 'deepika.raj@email.com',       '9876543032', 'Madurai, Tamil Nadu'),
('Akash Dubey',       '2002-10-04', 'Male',   'B.Sc CS', 2, 'akash.dubey@email.com',       '9876543033', 'Gwalior, MP'),
('Kritika Saxena',    '2002-02-21', 'Female', 'B.Sc CS', 2, 'kritika.saxena@email.com',    '9876543034', 'Meerut, UP'),
('Varun Malhotra',    '2001-05-10', 'Male',   'B.Sc CS', 3, 'varun.malhotra@email.com',    '9876543035', 'Chandigarh, Punjab'),
('Shreya Kapoor',     '2001-09-29', 'Female', 'B.Sc CS', 3, 'shreya.kapoor@email.com',     '9876543036', 'Ludhiana, Punjab'),
('Mohit Sinha',       '2003-12-18', 'Male',   'BCA',     1, 'mohit.sinha@email.com',       '9876543037', 'Muzaffarpur, Bihar'),
('Neha Tripathi',     '2002-07-07', 'Female', 'BCA',     2, 'neha.tripathi@email.com',     '9876543038', 'Gorakhpur, UP'),
('Rajesh Nambiar',    '2001-10-26', 'Male',   'B.Com',   3, 'rajesh.nambiar@email.com',    '9876543039', 'Thrissur, Kerala'),
('Swati Pande',       '2003-04-15', 'Female', 'B.Sc IT', 1, 'swati.pande@email.com',       '9876543040', 'Nagpur, Maharashtra'),
('Kunal Bhatt',       '2003-07-04', 'Male',   'B.Sc CS', 1, 'kunal.bhatt@email.com',       '9876543041', 'Vadodara, Gujarat'),
('Aishwarya Kumar',   '2003-10-23', 'Female', 'B.Sc CS', 1, 'aishwarya.kumar@email.com',   '9876543042', 'Mysuru, Karnataka'),
('Tushar Banerjee',   '2002-02-11', 'Male',   'B.Sc CS', 2, 'tushar.banerjee@email.com',   '9876543043', 'Asansol, WB'),
('Poornima Hegde',    '2002-06-30', 'Female', 'B.Sc CS', 2, 'poornima.hegde@email.com',    '9876543044', 'Hubli, Karnataka'),
('Shubham Rastogi',   '2001-12-19', 'Male',   'B.Sc CS', 3, 'shubham.rastogi@email.com',   '9876543045', 'Bareilly, UP'),
('Madhuri Chavan',    '2001-03-08', 'Female', 'B.Sc CS', 3, 'madhuri.chavan@email.com',    '9876543046', 'Kolhapur, Maharashtra'),
('Gaurav Thakur',     '2003-08-27', 'Male',   'BCA',     1, 'gaurav.thakur@email.com',     '9876543047', 'Shimla, HP'),
('Prachi Wagh',       '2002-04-16', 'Female', 'BCA',     2, 'prachi.wagh@email.com',       '9876543048', 'Nashik, Maharashtra'),
('Sanjay Pillai',     '2001-08-05', 'Male',   'B.Com',   3, 'sanjay.pillai@email.com',     '9876543049', 'Kollam, Kerala'),
('Varsha Tomar',      '2003-11-24', 'Female', 'B.Sc IT', 1, 'varsha.tomar@email.com',      '9876543050', 'Ghaziabad, UP'),
('Abhishek Jain',     '2003-02-13', 'Male',   'B.Sc CS', 1, 'abhishek.jain@email.com',     '9876543051', 'Jodhpur, Rajasthan'),
('Richa Srivastava',  '2003-05-02', 'Female', 'B.Sc CS', 1, 'richa.srivastava@email.com',  '9876543052', 'Allahabad, UP'),
('Vivek Anand',       '2002-08-21', 'Male',   'B.Sc CS', 2, 'vivek.anand@email.com',       '9876543053', 'Patna, Bihar'),
('Megha Sethi',       '2002-12-10', 'Female', 'B.Sc CS', 2, 'megha.sethi@email.com',       '9876543054', 'Faridabad, Haryana'),
('Nitin Solanki',     '2001-04-29', 'Male',   'B.Sc CS', 3, 'nitin.solanki@email.com',     '9876543055', 'Rajkot, Gujarat'),
('Sonali Bhat',       '2001-07-18', 'Female', 'B.Sc CS', 3, 'sonali.bhat@email.com',       '9876543056', 'Jammu, J&K'),
('Deepak Rawat',      '2003-10-07', 'Male',   'BCA',     1, 'deepak.rawat@email.com',       '9876543057', 'Dehradun, Uttarakhand'),
('Aarti Misra',       '2002-03-26', 'Female', 'BCA',     2, 'aarti.misra@email.com',       '9876543058', 'Bhopal, MP'),
('Sumit Chatterjee',  '2001-06-15', 'Male',   'B.Com',   3, 'sumit.chatterjee@email.com',  '9876543059', 'Siliguri, WB'),
('Preeti Naik',       '2003-09-04', 'Female', 'B.Sc IT', 1, 'preeti.naik@email.com',       '9876543060', 'Panaji, Goa'),
('Rohit Shinde',      '2003-01-23', 'Male',   'B.Sc CS', 1, 'rohit.shinde@email.com',      '9876543061', 'Pune, Maharashtra'),
('Ruchika Arora',     '2003-04-12', 'Female', 'B.Sc CS', 1, 'ruchika.arora@email.com',     '9876543062', 'Gurugram, Haryana'),
('Saurabh Pandey',    '2002-07-31', 'Male',   'B.Sc CS', 2, 'saurabh.pandey@email.com',    '9876543063', 'Varanasi, UP'),
('Bhavna Yadav',      '2002-11-19', 'Female', 'B.Sc CS', 2, 'bhavna.yadav@email.com',      '9876543064', 'Agra, UP'),
('Kartik Oberoi',     '2001-02-08', 'Male',   'B.Sc CS', 3, 'kartik.oberoi@email.com',     '9876543065', 'Amritsar, Punjab'),
('Aparna Menon',      '2001-05-27', 'Female', 'B.Sc CS', 3, 'aparna.menon@email.com',      '9876543066', 'Kochi, Kerala'),
('Himanshu Tiwari',   '2003-08-16', 'Male',   'BCA',     1, 'himanshu.tiwari@email.com',   '9876543067', 'Lucknow, UP'),
('Chandni Verma',     '2002-02-05', 'Female', 'BCA',     2, 'chandni.verma@email.com',     '9876543068', 'Meerut, UP'),
('Pankaj Rathore',    '2001-05-24', 'Male',   'B.Com',   3, 'pankaj.rathore@email.com',    '9876543069', 'Jaipur, Rajasthan'),
('Swapna Pillai',     '2003-08-13', 'Female', 'B.Sc IT', 1, 'swapna.pillai@email.com',     '9876543070', 'Thiruvananthapuram, Kerala'),
('Ankit Sharma',      '2003-11-02', 'Male',   'B.Sc CS', 1, 'ankit.sharma@email.com',      '9876543071', 'Jaipur, Rajasthan'),
('Rupali Deshpande',  '2004-01-21', 'Female', 'B.Sc CS', 1, 'rupali.deshpande@email.com',  '9876543072', 'Aurangabad, Maharashtra'),
('Gaurav Negi',       '2002-04-10', 'Male',   'B.Sc CS', 2, 'gaurav.negi@email.com',       '9876543073', 'Dehradun, Uttarakhand'),
('Komal Soni',        '2002-07-29', 'Female', 'B.Sc CS', 2, 'komal.soni@email.com',        '9876543074', 'Udaipur, Rajasthan'),
('Sachin Pawar',      '2001-10-18', 'Male',   'B.Sc CS', 3, 'sachin.pawar@email.com',      '9876543075', 'Pune, Maharashtra'),
('Jyoti Kumari',      '2001-01-07', 'Female', 'B.Sc CS', 3, 'jyoti.kumari@email.com',      '9876543076', 'Patna, Bihar'),
('Harshit Goel',      '2003-03-26', 'Male',   'BCA',     1, 'harshit.goel@email.com',      '9876543077', 'Noida, UP'),
('Sunita Rajan',      '2002-06-15', 'Female', 'BCA',     2, 'sunita.rajan@email.com',      '9876543078', 'Coimbatore, Tamil Nadu'),
('Manoj Bhardwaj',    '2001-09-04', 'Male',   'B.Com',   3, 'manoj.bhardwaj@email.com',    '9876543079', 'Kanpur, UP'),
('Archana Nambiar',   '2003-11-23', 'Female', 'B.Sc IT', 1, 'archana.nambiar@email.com',   '9876543080', 'Palakkad, Kerala'),
('Vikas Tomar',       '2004-02-11', 'Male',   'B.Sc CS', 1, 'vikas.tomar@email.com',       '9876543081', 'Ghaziabad, UP'),
('Nisha Kulkarni',    '2004-05-01', 'Female', 'B.Sc CS', 1, 'nisha.kulkarni@email.com',    '9876543082', 'Pune, Maharashtra'),
('Ashish Dubey',      '2002-07-20', 'Male',   'B.Sc CS', 2, 'ashish.dubey@email.com',      '9876543083', 'Jabalpur, MP'),
('Priyanka Rao',      '2002-10-09', 'Female', 'B.Sc CS', 2, 'priyanka.rao@email.com',      '9876543084', 'Vijayawada, AP'),
('Shivam Agarwal',    '2001-12-28', 'Male',   'B.Sc CS', 3, 'shivam.agarwal@email.com',    '9876543085', 'Agra, UP'),
('Vandana Mishra',    '2001-03-17', 'Female', 'B.Sc CS', 3, 'vandana.mishra@email.com',    '9876543086', 'Allahabad, UP'),
('Lalit Chauhan',     '2003-06-06', 'Male',   'BCA',     1, 'lalit.chauhan@email.com',     '9876543087', 'Dehradun, Uttarakhand'),
('Rekha Singh',       '2002-08-25', 'Female', 'BCA',     2, 'rekha.singh@email.com',       '9876543088', 'Lucknow, UP'),
('Dinesh Nair',       '2001-11-14', 'Male',   'B.Com',   3, 'dinesh.nair@email.com',       '9876543089', 'Thiruvananthapuram, Kerala'),
('Preethi Suresh',    '2004-02-02', 'Female', 'B.Sc IT', 1, 'preethi.suresh@email.com',    '9876543090', 'Chennai, Tamil Nadu'),
('Rajat Kapoor',      '2004-04-22', 'Male',   'B.Sc CS', 1, 'rajat.kapoor@email.com',      '9876543091', 'Delhi'),
('Mansi Jain',        '2004-07-11', 'Female', 'B.Sc CS', 1, 'mansi.jain@email.com',        '9876543092', 'Surat, Gujarat'),
('Saurav Ghosh',      '2002-09-30', 'Male',   'B.Sc CS', 2, 'saurav.ghosh@email.com',      '9876543093', 'Kolkata, WB'),
('Tejal Patil',       '2003-01-18', 'Female', 'B.Sc CS', 2, 'tejal.patil@email.com',       '9876543094', 'Pune, Maharashtra'),
('Aman Srivastava',   '2001-04-07', 'Male',   'B.Sc CS', 3, 'aman.srivastava@email.com',   '9876543095', 'Kanpur, UP'),
('Geeta Sharma',      '2001-06-26', 'Female', 'B.Sc CS', 3, 'geeta.sharma@email.com',      '9876543096', 'Jaipur, Rajasthan'),
('Praveen Kumar',     '2003-09-15', 'Male',   'BCA',     1, 'praveen.kumar@email.com',     '9876543097', 'Bengaluru, Karnataka'),
('Smita Deshpande',   '2002-12-04', 'Female', 'BCA',     2, 'smita.deshpande@email.com',   '9876543098', 'Nagpur, Maharashtra'),
('Yogesh Bhatia',     '2002-02-22', 'Male',   'B.Com',   3, 'yogesh.bhatia@email.com',     '9876543099', 'Chandigarh, Punjab'),
('Asha Krishnan',     '2004-05-12', 'Female', 'B.Sc IT', 1, 'asha.krishnan@email.com',     '9876543100', 'Kochi, Kerala');

-- ── Fee Payments (realistic mix) ─────────────────────────────
INSERT INTO fee_payments (student_id, amount, payment_date, payment_mode, remarks)
SELECT
    s.student_id,
    CASE WHEN random() < 0.4 THEN 50000
         WHEN random() < 0.6 THEN 25000
         ELSE 10000 END,
    CURRENT_DATE - (random() * 180)::int,
    (ARRAY['Cash','Online Transfer','Cheque','DD'])[floor(random()*4+1)::int],
    'Fee payment'
FROM students s
WHERE random() < 0.85;

-- Second instalment for some students
INSERT INTO fee_payments (student_id, amount, payment_date, payment_mode, remarks)
SELECT
    s.student_id,
    25000,
    CURRENT_DATE - (random() * 60)::int,
    (ARRAY['Cash','Online Transfer','Cheque','DD'])[floor(random()*4+1)::int],
    'Second instalment'
FROM students s
WHERE random() < 0.3;

-- ── Attendance for all students (last 10 days, 3 subjects) ───
INSERT INTO attendance (student_id, subject_id, date, status)
SELECT
    s.student_id,
    sub.subject_id,
    CURRENT_DATE - d.day_offset,
    CASE WHEN random() < 0.82 THEN 'Present' ELSE 'Absent' END
FROM students s
CROSS JOIN subjects sub
CROSS JOIN (
    SELECT generate_series(0,9) AS day_offset
) d
ON CONFLICT (student_id, subject_id, date) DO NOTHING;

-- ── Results for students 1–60 ─────────────────────────────────
INSERT INTO results (student_id, subject_id, exam_type, marks_obtained, max_marks)
SELECT
    s.student_id,
    sub.subject_id,
    exam.exam_type,
    GREATEST(20, LEAST(
        CASE exam.exam_type WHEN 'Internal' THEN 50 ELSE 100 END,
        floor(random() *
            CASE exam.exam_type WHEN 'Internal' THEN 50 ELSE 100 END
        + 30)::int
    )),
    CASE exam.exam_type WHEN 'Internal' THEN 50 ELSE 100 END
FROM students s
CROSS JOIN subjects sub
CROSS JOIN (VALUES ('Internal'), ('External')) AS exam(exam_type)
WHERE s.student_id <= 60
ON CONFLICT (student_id, subject_id, exam_type) DO NOTHING;

-- ── Verify ────────────────────────────────────────────────────
SELECT 'students'     AS tbl, COUNT(*) FROM students
UNION ALL
SELECT 'fee_payments', COUNT(*) FROM fee_payments
UNION ALL
SELECT 'attendance',   COUNT(*) FROM attendance
UNION ALL
SELECT 'results',      COUNT(*) FROM results;
