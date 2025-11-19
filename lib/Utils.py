import smtplib
from email.mime.text import MIMEText
from Config import EMAIL_SETTINGS

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SETTINGS["username"]
    msg['To'] = EMAIL_SETTINGS["to"]

    server = smtplib.SMTP(EMAIL_SETTINGS["smtp_server"], EMAIL_SETTINGS["smtp_port"])
    server.starttls()
    server.login(EMAIL_SETTINGS["username"], EMAIL_SETTINGS["password"])
    server.send_message(msg)
    server.quit()
