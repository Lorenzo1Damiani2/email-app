import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from flask import Flask, jsonify
import logging
import requests
import time

# Configure logging to log to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

df = pd.read_csv('data_with_dates.csv')
df["date"] = pd.to_datetime(df["date"])

app = Flask(__name__)

def send_email():
    logging.info("send_email function started")
    
    today = datetime.today().date()
    logging.info(f"Today's date: {today}")
    
    word_of_the_day_row = df[df['date'].dt.date == today]
    logging.info(f"Word of the day row: {word_of_the_day_row}")
    
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
            logging.info("Connecting to email server")
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

@app.route('/')
def index():
    logging.info("Index route accessed")
    return jsonify({"message": "Email has been sent!"})

@app.route('/send_email')
def trigger_email():
    logging.info("/send_email route accessed")
    send_email()
    return jsonify({"message": "Email sent successfully!"})

if __name__ == "__main__":
    logging.info("Starting Flask app")
    app.run(debug=False, host='0.0.0.0', port=8080)
    
    # Wait for a few seconds to ensure the server is fully started
    time.sleep(5)

    # Trigger the send_email endpoint
    try:
        response = requests.get('http://127.0.0.1:8080/send_email')
        if response.status_code == 200:
            logging.info("Email triggered successfully at startup")
        else:
            logging.error(f"Failed to trigger email at startup: {response.status_code}")
    except Exception as e:
        logging.error(f"Exception occurred while triggering email at startup: {e}")
