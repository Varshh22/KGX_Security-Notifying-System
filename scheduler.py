import schedule
import time
from models import db, Attendance
import generate_pdf
import email_service
from flask import Flask
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Function to check if tomorrow is a public holiday


def is_tomorrow_public_holiday():
    # Add logic to check if tomorrow is a public holiday
    # Example list of public holidays (dates should be in 'YYYY-MM-DD' format)
    public_holidays = [
    "2024-01-01",
    "2024-06-11",
    "2024-01-14",
    "2024-01-26",
    "2024-04-12",
    "2024-04-14",
    "2024-05-01",
    "2024-08-15",
    "2024-08-23",
    "2024-10-02",
    "2024-10-22",
    "2024-12-25",
    "2024-01-07", "2024-01-14", "2024-01-21", "2024-01-28",
    "2024-02-04", "2024-02-11", "2024-02-18", "2024-02-25",
    "2024-03-03", "2024-03-10", "2024-03-17", "2024-03-24", "2024-03-31",
    "2024-04-07", "2024-04-14", "2024-04-21", "2024-04-28",
    "2024-05-05", "2024-05-12", "2024-05-19", "2024-05-26",
    "2024-06-02", "2024-06-09", "2024-06-16", "2024-06-23", "2024-06-30",
    "2024-07-07", "2024-07-14", "2024-07-21", "2024-07-28",
    "2024-08-04", "2024-08-11", "2024-08-18", "2024-08-25",
    "2024-09-01", "2024-09-08", "2024-09-15", "2024-09-22", "2024-09-29",
    "2024-10-06", "2024-10-13", "2024-10-20", "2024-10-27",
    "2024-11-03", "2024-11-10", "2024-11-17", "2024-11-24",
    "2024-12-01", "2024-12-08", "2024-12-15", "2024-12-22", "2024-12-29",
]

    tomorrow = datetime.now().date() + timedelta(days=1)
    return tomorrow.strftime('%Y-%m-%d') in public_holidays

def job():
    if is_tomorrow_public_holiday():
        with app.app_context():
            data = Attendance.query.all()
            pdf_filename = generate_pdf.generate_pdf(data)
            email_service.send_email(pdf_filename)

# Schedule the job to run daily at a specific time
schedule_time = "22:01"  # Set the time you want the job to run
schedule.every().day.at(schedule_time).do(job)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    while True:
        schedule.run_pending()
        time.sleep(1)
