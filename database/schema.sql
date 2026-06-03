-- =========================================
-- STUDENT REGISTRATION TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_number TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    supervisor TEXT NOT NULL
);

-- =========================================
-- ASSIGNMENT SUBMISSIONS TABLE
-- =========================================
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_number TEXT NOT NULL,
    name TEXT NOT NULL,
    supervisor TEXT NOT NULL,
    file_path TEXT NOT NULL,
    upload_time TEXT NOT NULL
);
