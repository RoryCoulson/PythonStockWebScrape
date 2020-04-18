import smtplib
import os
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')    # think this is his weird way of getting his info..
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Want some stocks?'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS   # or another email..
msg.set_content(EMAIL_ADDRESS)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    smtp.send_message(msg)

