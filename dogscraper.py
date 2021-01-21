import re
import requests
from bs4 import BeautifulSoup

URL = 'https://www.pets4homes.co.uk/search/?type_id=3&breed_id=142&advert_type=0&results=20&sort=datenew'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())
#all_text = soup.get_text()


#listings = soup.find_all('div', class_=re.compile('profile-listing-updated'))
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
        break
print(message)