import os
import smtplib
import ssl

def send_email(recipient_email, message):
    sender_email = "sam.seed.dev@gmail.com"
    port = 465  # For SSL
    password = os.environ.get('google_password')

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("sam.seed.dev@gmail.com", password)
        server.sendmail(sender_email, recipient_email, message)