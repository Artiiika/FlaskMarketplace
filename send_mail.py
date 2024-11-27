import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
def send_mail(subject, email, message):
    sender = os.getenv('SMTP_EMAIL')
    password = os.getenv('SMTP_PASSWORD')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['To'] = email
        server.sendmail(sender, email, msg.as_string())
        server.quit()
        return 'Message was send'

    except Exception as _ex:
        return f'{_ex}\nCheck ur login or password from email!'