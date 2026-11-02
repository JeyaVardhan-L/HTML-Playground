"""
capture_evidence.py
Starts Flask and Django development servers, captures real browser screenshots
using Playwright, and saves them for the assignment report documentation.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
FLASK_DIR = BASE_DIR / "flask-app"
DJANGO_DIR = BASE_DIR / "django-app"
DOCS_DIR = BASE_DIR / "documentation"
SCREENSHOTS_DIR = DOCS_DIR / "screenshots"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

PYTHON_EXE = sys.executable

def capture_flask():
    print(">>> Starting Flask server on http://127.0.0.1:5001...")
    flask_proc = subprocess.Popen(
        [PYTHON_EXE, "-c", "import sys; sys.path.insert(0, r'" + str(FLASK_DIR) + "'); import app; app.app.run(host='127.0.0.1', port=5001, debug=False)"],
        cwd=str(FLASK_DIR)
    )
    time.sleep(2.5)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 820})
            print(">>> Navigating to Flask application...")
            page.goto("http://127.0.0.1:5001/", wait_until="networkidle")
            page.wait_for_selector("table")
            time.sleep(1)
            
            output_path = SCREENSHOTS_DIR / "flask_student_records.png"
            page.screenshot(path=str(output_path), full_page=False)
            print(f">>> Flask screenshot saved to: {output_path}")
            browser.close()
    finally:
        flask_proc.terminate()
        try:
            flask_proc.wait(timeout=3)
        except Exception:
            flask_proc.kill()
        print(">>> Flask server stopped.")

def capture_django():
    print(">>> Starting Django server on http://127.0.0.1:8001...")
    django_proc = subprocess.Popen(
        [PYTHON_EXE, "manage.py", "runserver", "127.0.0.1:8001", "--noreload"],
        cwd=str(DJANGO_DIR)
    )
    time.sleep(3)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 820})
            print(">>> Navigating to Django application...")
            page.goto("http://127.0.0.1:8001/", wait_until="networkidle")
            page.wait_for_selector("table")
            time.sleep(1)
            
            output_path = SCREENSHOTS_DIR / "django_student_records.png"
            page.screenshot(path=str(output_path), full_page=False)
            print(f">>> Django screenshot saved to: {output_path}")
            browser.close()
    finally:
        django_proc.terminate()
        try:
            django_proc.wait(timeout=3)
        except Exception:
            django_proc.kill()
        print(">>> Django server stopped.")

if __name__ == "__main__":
    capture_flask()
    time.sleep(1)
    capture_django()
    print(">>> All screenshots captured successfully!")
