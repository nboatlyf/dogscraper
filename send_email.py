import smtplib, ssl

sender_email = "sam.seed.dev@gmail.com"
receiver_email = "s.seed@protonmail.ch"
message = '''\
Subject: Dog alert!

There's a new goddam dog in town. Woof woof!'''

port = 465  # For SSL
password = input("Type your password and press enter: ")

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("sam.seed.dev@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)