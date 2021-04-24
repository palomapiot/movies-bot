# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import requests
import json
from urllib.request import Request, urlopen

BASE_URL = 'https://api.trakt.tv'
TRAKT_URL = 'https://trakt.tv'



class ActionValidateMovieForm(Action):

    def name(self) -> Text:
        return "validate_movie_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot('movie')
        if (movie_name is not None):
            movie_name = movie_name.replace(' ', '%20')

            # Auth trakt
            auth()

            # Search movie
            headers = {
                'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': CLIENT_ID
            }
            request = Request(BASE_URL + '/search/movie?query=' + movie_name, headers=headers)
            response_body = urlopen(request)
            movies = json.load(response_body)
            response_movies = [movie['movie']['title'] for movie in movies]
            buttons = []
            for movie in movies:
                button = {
                    "title": movie['movie']['title'] + ' ' + str(movie['movie']['year']),
                    "payload": "/select_movie{\"selected_movie\": \"" + str(movie['movie']['ids']['trakt']) + "\"}"
                }
                buttons.append(button)

            dispatcher.utter_message(text="Found the movies:", buttons=buttons)
            return [SlotSet("movie", response_movies if response_movies is not None else [])]
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find that movie.")
            return []

class ActionValidateDownloadMovieForm(Action):

    def name(self) -> Text:
        return "validate_download_movie_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_id = tracker.get_slot('selected_movie')
        if (movie_id is not None):
            # Get movie by ID
            headers = {
                'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': CLIENT_ID
            }
            movie_request = Request(BASE_URL + '/search/trakt/' + movie_id + '?type=movie', headers=headers)
            movie_body = urlopen(movie_request)
            movie_result = json.load(movie_body)
            movie = [m['movie'] for m in movie_result]
            print(movie_result)
            movie_slug = movie_result[0]['movie']['ids']['slug']
            print(movie_slug)
            
            # Send movie to a telegram chat
            telegram_bot_sendtext("Please download the movie: " + TRAKT_URL + '/movies/' + movie_slug)

            dispatcher.utter_message(text="Starting to download your movie! Will be available in Diegoflix soon.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find that movie.")
        return []

def auth():
    # Auth trakt
    headers = {
        'Content-Type': 'application/json'
    }
    request = Request(BASE_URL + '/oauth/authorize', headers=headers)
    response_body = urlopen(request).read()

def telegram_bot_sendtext(bot_message):
   send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()