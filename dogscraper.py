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

#prog = re.compile('\n\xa0\xa0(?P<time_count>\d+)\s[a-z]+')
updated_time_matcher = re.compile('(?P<time_count>\d+)\s(?P<time_type>[a-z]+)')

message = 'No new dogs :('
for listing in listings:

    updated_time = updated_time_matcher.search(listing.string)

    time_count = int(updated_time.group('time_count'))
    time_type = updated_time.group('time_type')

    if time_type in ('minute', 'minutes'):
        if time_count <= 10:
            message = '''There's a new dog in town!'''
            break

print(message)

