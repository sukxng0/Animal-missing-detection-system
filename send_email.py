import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert_email():
    sender_email = "wlsaud031206@gmail.com"
    receiver_email = "skk9568@naver.com"
    app_password = "ynsf xcdt bqov qshs"  # App password (16 digits)

    subject = "Pet Alert: Animal Missing!"
    body = "Warning: The monitored pet has disappeared from the camera frame."

    # Create email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Alert email sent successfully.")
    except Exception as e:
        print("Email sending failed:", e)
