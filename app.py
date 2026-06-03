import os
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.utils import secure_filename

# -----------------------------
# APP SETUP
# -----------------------------
app = Flask(__name__)
app.secret_key = "assignment_portal_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATA_FILE = os.path.join(BASE_DIR, "data", "students.csv")
DB_FILE = os.path.join(BASE_DIR, "database", "app.db")

ALLOWED_EXTENSIONS = {"pdf", "ppt", "pptx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -----------------------------
# ENSURE DIRECTORIES EXIST
# -----------------------------
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)


# -----------------------------
# LOAD STUDENTS CSV
# -----------------------------
try:
    students_df = pd.read_csv(DATA_FILE)
except Exception:
    students_df = pd.DataFrame(columns=["admission_number", "name", "supervisor"])


def is_valid_student(admission_number):
    return admission_number in students_df["admission_number"].values


def get_student_info(admission_number):
    row = students_df[students_df["admission_number"] == admission_number]
    if not row.empty:
        return row.iloc[0].to_dict()
    return None


# -----------------------------
# DATABASE INIT
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            admission_number TEXT,
            supervisor TEXT,
            file_path TEXT,
            upload_time TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# -----------------------------
# HELPERS
# -----------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":

        name = request.form.get("name")
        admission_number = request.form.get("admission_number")

        # Validate student
        if not is_valid_student(admission_number):
            flash("Invalid admission number.", "error")
            return redirect(url_for("submit"))

        student_info = get_student_info(admission_number)

        # File check
        if "file" not in request.files:
            flash("No file uploaded.", "error")
            return redirect(url_for("submit"))

        file = request.files["file"]

        if file.filename == "":
            flash("No file selected.", "error")
            return redirect(url_for("submit"))

        if not allowed_file(file.filename):
            flash("Only PDF, PPT, PPTX allowed.", "error")
            return redirect(url_for("submit"))

        # Secure filename
        filename = secure_filename(file.filename)

        # Create unique folder per submission
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        student_folder = os.path.join(
            UPLOAD_FOLDER,
            f"{admission_number}_{timestamp}"
        )

        os.makedirs(student_folder, exist_ok=True)

        file_path = os.path.join(student_folder, filename)
        file.save(file_path)

        # Save to database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO submissions (
                name,
                admission_number,
                supervisor,
                file_path,
                upload_time
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            student_info["name"],
            admission_number,
            student_info["supervisor"],
            file_path,
            timestamp
        ))

        conn.commit()
        conn.close()

        flash("Submission successful!", "success")
        return redirect(url_for("submit"))

    return render_template("submit.html")


@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM submissions ORDER BY upload_time DESC")
    submissions = cursor.fetchall()

    conn.close()

    return render_template("admin.html", submissions=submissions)


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)