# Hostel Management Automation Bot

A hostel complaint management system that automates complaint submission, ticket generation, database logging, and email notification.

## Project Overview

This project is based on the submitted project report. The system is designed around a UiPath RPA workflow that reads hostel complaint emails, extracts complaint details, classifies priority, generates a unique ticket ID, stores ticket information, and sends acknowledgement/notification emails.

A Flask prototype is also included in this repository to demonstrate the complaint form, ticket generation, SQLite storage, and email notification workflow.

## Main Features

- Student hostel complaint submission
- Unique ticket ID generation
- Complaint issue categorization
- Priority classification
- SQLite ticket storage
- Automated email notification
- Complaint status tracking
- Simple web interface
- UiPath workflow concept for Gmail-based automation

## Technology Stack

- Python
- Flask
- SQLite
- HTML/CSS/JavaScript
- SMTP email
- UiPath Studio
- Gmail / Google Workspace

## Project Structure

```text
hostel-management-automation-bot/
├── backend/
│   └── app.py
├── frontend/
│   └── index.html
├── data/
│   └── .gitkeep
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Run the Flask Prototype

### 1. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure email

Copy `.env.example` to `.env` and add your own email configuration.

**Never commit `.env` or real passwords/API keys to GitHub.**

### 4. Start the application

```bash
python backend/app.py
```

Open:

```text
http://127.0.0.1:5000
```

## UiPath Workflow

The report describes a workflow using Google Workspace Scope, Get Email List, For Each, Assign, If, Append Line, and Send SMTP activities. The workflow extracts student information, checks complaint keywords, assigns priority, generates a ticket ID, stores the record, and sends notifications.

## Future Scope

- AI/NLP-based complaint classification
- Priority escalation
- Hostel attendance automation
- Room allocation
- Fee reminders
- Real-time dashboard
- WhatsApp/SMS notifications
- Student identity verification
- Complaint feedback and ratings

## Security Note

The original report contains an email credential in its code appendix. Do not copy that credential into this repository. Use environment variables and revoke/rotate any real credential that may have been exposed.

## Authors

- Abirami S
- Adithi Shree V

Panimalar Engineering College, Department of Computer Science and Engineering.
