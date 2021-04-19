# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import json
from urllib.request import Request, urlopen
 
class ActionValidateMovieForm(Action):

    def name(self) -> Text:
        return "validate_movie_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot('movie')
        movie_name = movie_name.replace(' ', '%20')

        # Auth trakt
        headers = {
            'Content-Type': 'application/json'
        }
        request = Request('https://api.trakt.tv/oauth/authorize', headers=headers)
        response_body = urlopen(request).read()

        # Search movie
        headers = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': '99c154b68b67951f7a21354baa5f0afb68a9207e4c60f96bf08af0500f4602c5' # client_id
        }
        request = Request('https://api.trakt.tv/search/movie?query=' + movie_name, headers=headers)
        response_body = urlopen(request)
        movies = json.load(response_body)
        buttons = []
        for movie in movies:
            button = {
                "title": movie['movie']['title'],
                "payload": "/select_movie"
            }
            buttons.append(button)
        #buttons = [movie['movie']['title'] for movie in movies]

        dispatcher.utter_message(text="Found the movies:", buttons=buttons)

        return []
