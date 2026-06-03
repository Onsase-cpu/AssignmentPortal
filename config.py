import os

# -----------------------------
# BASE DIRECTORY
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------
DATABASE_PATH = os.path.join(BASE_DIR, "database", "app.db")


# -----------------------------
# UPLOAD CONFIGURATION
# -----------------------------
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Maximum file size (in bytes)
# 10 MB default
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "ppt", "pptx"}


# -----------------------------
# STUDENT DATA SOURCE
# -----------------------------
STUDENTS_FILE = os.path.join(BASE_DIR, "data", "students.csv")


# -----------------------------
# FLASK SECURITY SETTINGS
# -----------------------------
SECRET_KEY = "change_this_to_a_secure_random_key"


# -----------------------------
# APPLICATION SETTINGS
# -----------------------------
APP_NAME = "Assignment Submission Portal"
DEBUG_MODE = True


# -----------------------------
# HELPER FUNCTION
# -----------------------------
def get_config():
    """
    Returns all configuration values as a dictionary.
    Useful for debugging or future admin dashboards.
    """
    return {
        "database_path": DATABASE_PATH,
        "upload_folder": UPLOAD_FOLDER,
        "max_content_length": MAX_CONTENT_LENGTH,
        "allowed_extensions": list(ALLOWED_EXTENSIONS),
        "students_file": STUDENTS_FILE,
        "app_name": APP_NAME,
        "debug_mode": DEBUG_MODE
    }