import os

from breed import Breed
from send_email import send_email

english_bulldog_id = 126
golder_retriever_id = 142
goldendoodle_id = 143
jack_russell_id = 157
labrador_retriever_id = 163
scottish_terrier_id = 208
yorkshire_terrier_id = 230
mixed_breed_id = 451
italian_greyhound_id = 470

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