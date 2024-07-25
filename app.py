import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import logging

df = pd.read_csv('data_with_dates.csv')
df["date"] = pd.to_datetime(df["date"])

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def send_email():
    today = datetime.today().date()
    word_of_the_day_row = df[df['date'].dt.date == today]

    if not word_of_the_day_row.empty:
        word_of_the_day = word_of_the_day_row['catalan'].values[0]
        meaning = word_of_the_day_row['english'].values[0]
    else:
        word_of_the_day = None
        meaning = None

    logging.info(f"Word of the Day (Catalan): {word_of_the_day}")
    logging.info(f"Meaning (English): {meaning}")

    email_content = f"Word of the Day: {word_of_the_day}\nMeaning: {meaning}"

    sender_email = "lorenzodamiani06@gmail.com"
    receiver_email = "damianilorenzo06@gmail.com"
    password = "xwsl fvio vzpu xcwn"

    msg = MIMEText(email_content)
    msg['Subject'] = f"Word of the Day: {word_of_the_day}"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

@app.route('/')
def index():
    return jsonify({"message": "Scheduler is running. Email will be sent as per schedule."})

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email, 'cron', hour=8, minute=0)
    scheduler.start()

    try:
        app.run(debug=True, host='0.0.0.0', port=8080)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
