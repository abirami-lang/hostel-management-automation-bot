import os
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "complaints.db")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__)


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                room TEXT NOT NULL,
                issue TEXT NOT NULL,
                complaint TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def classify_priority(issue, complaint):
    text = f"{issue} {complaint}".lower()
    urgent_words = ["urgent", "emergency", "leakage", "power failure", "danger"]
    if any(word in text for word in urgent_words):
        return "High"
    return "Normal"


def send_notification(name, email, ticket_id, room, issue, complaint, priority):
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")
    receiver = os.getenv("RECEIVER_EMAIL")

    # Email is optional for local/demo use.
    if not sender or not password or not receiver:
        return False

    body = f"""Dear {name},

Your hostel complaint has been registered successfully.

Ticket ID: {ticket_id}
Student Name: {name}
Room/Block: {room}
Issue Type: {issue}
Description: {complaint}
Priority: {priority}
Status: Open

Hostel Management Team
"""

    message = MIMEText(body)
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = f"Hostel Complaint Ticket: {ticket_id}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(message)
        return True
    except Exception as exc:
        app.logger.warning("Email notification failed: %s", exc)
        return False


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.post("/submit")
def submit():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    room = data.get("room", "").strip()
    issue = data.get("issue", "").strip()
    complaint = data.get("complaint", "").strip()

    if not all([name, email, room, issue, complaint]):
        return jsonify({"message": "Please fill all fields."}), 400

    priority = classify_priority(issue, complaint)
    timestamp = datetime.now()
    ticket_id = "TKT-" + timestamp.strftime("%Y%m%d%H%M%S%f")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO complaints
            (ticket_id, name, email, room, issue, complaint, priority, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id, name, email, room, issue, complaint,
            priority, "Open", timestamp.isoformat(timespec="seconds")
        ))
        conn.commit()

    email_sent = send_notification(
        name, email, ticket_id, room, issue, complaint, priority
    )

    return jsonify({
        "message": "Complaint submitted successfully!",
        "ticket_id": ticket_id,
        "name": name,
        "room": room,
        "issue": issue,
        "priority": priority,
        "status": "Open",
        "email_notification_sent": email_sent
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
