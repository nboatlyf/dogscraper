from bs4 import BeautifulSoup
import re
import requests

from breed_index import breed_index

class Breed:

    def __init__(self, breed_id):
        self.id = breed_id
        self.name = breed_index[str(breed_id)]
        self.URL = self.generate_URL(breed_id)
        self.post_times = self.get_post_times(breed_id)
        self.minutes_since_last_post = self.post_times[0]

    def generate_URL(self, breed_id):
        return f'''https://www.pets4homes.co.uk/search/?type_id=3&breed_id={breed_id}&advert_type=0&results=20&sort=datenew'''

    def get_post_times(self, breed_id):

        def get_raw_post_times(breed_id):        
            page = requests.get(self.URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            raw_post_times = soup.find_all('div', class_=re.compile('profile-listing-updated'))
            return raw_post_times

        def parse_raw_post_times(raw_post_times, time_pattern):
            post_times = []
            time_parser = re.compile(time_pattern)
            for raw_post_time in raw_post_times:
                parsed_post_time = time_parser.search(raw_post_time.string)
                time_count = int(parsed_post_time.group('time_count'))
                time_type = parsed_post_time.group('time_type')

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
                    ValueError('''Unknown time type. Please check how raw_post_time is being parsed.''')
                minutes_since_post = time_count * time_count_multiplier
                post_times.append(minutes_since_post)
            post_times.sort()
            return post_times
            
        raw_post_times = get_raw_post_times(breed_id)
        time_pattern = '(?P<time_count>\d+)\s(?P<time_type>[a-z]+)'
        post_times = parse_raw_post_times(raw_post_times, time_pattern)
        return post_times