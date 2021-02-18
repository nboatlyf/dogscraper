import os
import bs4
import re
import requests
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

english_bulldog_id = 126
golder_retriever_id = 142
goldendoodle_id = 143
jack_russell_id = 157
labrador_retriever_id = 163
scottish_terrier_id = 208
yorkshire_terrier_id = 230
mixed_breed_id = 451
italian_greyhound_id = 470

breed_index = {
    f'{english_bulldog_id}': 'English Bulldog',
    f'{golder_retriever_id}': 'Golden Retriever',
    f'{goldendoodle_id}': 'Goldendoodle',
    f'{jack_russell_id}': 'Jack Russell',
    f'{labrador_retriever_id}': 'Labrador Retriever',
    f'{scottish_terrier_id}': 'Scottish Terrier',
    f'{yorkshire_terrier_id}': 'Yorkshire Terrier',
    f'{mixed_breed_id}': 'Mixed Breed',
    f'{italian_greyhound_id}': 'Italian Greyhound'
}

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
            soup = bs4.BeautifulSoup(page.content, 'html.parser')
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


chosen_breeds = [scottish_terrier_id, yorkshire_terrier_id, italian_greyhound_id]

def scrape_dogs(time_period_to_check, *breed_ids):
    breeds_with_recent_posts = []
    for breed_id in breed_ids:
        breed = Breed(breed_id)
        if breed.minutes_since_last_post < time_period_to_check:
            breeds_with_recent_posts.append(breed)
    if len(breeds_with_recent_posts) == 0:
        print("No dogs :(")
        exit
    else:
        if len(breeds_with_recent_posts) == 1:
            dog_alert_text = "There's a new goddam dog in town. Woof woof!"
        elif len(breeds_with_recent_posts) > 1:
            dog_alert_text = "There's some new goddam dogs in town. Woof woof!"
        dog_alert_URLs = os.linesep.join([f"{breed.name}: {breed.URL}" for breed in breeds_with_recent_posts])
        dog_alert_message = f"""\
Subject: Dog alert!

{dog_alert_text}

{dog_alert_URLs}"""
        print(dog_alert_message)
        send_email('s.seed@protonmail.ch', dog_alert_message)
        send_email('rochelle_smith@hotmail.co.uk', dog_alert_message)

scrape_dogs(15, *chosen_breeds)