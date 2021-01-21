from bs4 import BeautifulSoup
import re
import requests
import smtplib
import ssl


def send_email(recipient_email, message):
    sender_email = "sam.seed.dev@gmail.com"

    port = 465  # For SSL
    password = 'donkeyelephant999dolphins'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("sam.seed.dev@gmail.com", password)
        server.sendmail(sender_email, recipient_email, message)


english_bulldog_id = 126
golder_retriever_id = 142
scottish_terrier_id = 208

URL = f'''https://www.pets4homes.co.uk/search/?type_id=3&breed_id={english_bulldog_id}&advert_type=0&results=20&sort=datenew'''
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

listings = soup.find_all('div', class_=re.compile('profile-listing-updated'))

time_parser = re.compile('(?P<time_count>\d+)\s(?P<time_type>[a-z]+)')

happy_message = '''\
Subject: Dog alert!

There's a new goddam dog in town. Woof woof!'''

sad_message = '''\
Subject: No new dogs :'(

Will we ever have a woofer to call our own?'''

message = sad_message
for listing in listings:

    updated_time = time_parser.search(listing.string)

    time_count = int(updated_time.group('time_count'))
    time_type = updated_time.group('time_type')

    if time_type in 'seconds':
        time_count_multiplier = 1 / 60
    elif time_type in 'minutes':
        time_count_multiplier = 1
    elif time_type in 'hours':
        time_count_multiplier = 60
    elif time_type in 'days':
        time_count_multiplier = 60 * 24
    elif time_type in 'months':
        time_count_multiplier = 60 * 24 * 30
    else:
        ValueError('''Unknown time type. Please check how 'listing updated time' is being parsed.''')
    minutes_since_update = time_count * time_count_multiplier

    print(f'''This listing was posted {str(time_count)} {time_type} ago. That's {minutes_since_update} minutes.''')
    if minutes_since_update < 0.5:
        message = happy_message
        send_email('s.seed@protonmail.ch', message)
        break

print(message)