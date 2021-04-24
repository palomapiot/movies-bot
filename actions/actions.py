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

CLIENT_ID = '99c154b68b67951f7a21354baa5f0afb68a9207e4c60f96bf08af0500f4602c5'
CLIENT_SECRET = 'xxxxx'
BASE_URL = 'https://api.trakt.tv'

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
            # Get bearer token
            #bearer_token = token()

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


            """# Add movie to Watchlist           
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + bearer_token,
                'trakt-api-version': '2',
                'trakt-api-key': CLIENT_ID
            }
            movies_body = {
                'movies': movie
            }
            watchlist_request = requests.post(BASE_URL + '/sync/watchlist', data=movies_body, headers=headers)"""
            # Send movie to a chat

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

"""def code():
    values =  {
        'client_id': CLIENT_ID
    }

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(BASE_URL + '/oauth/device/code', json=values, headers=headers).json()
    print(response)
    
    # todo: go to the verification url and enter user code

    return response.get('device_code')

def token():
    auth()          
    device_code = code()

    values = {
        "code": device_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    print(values)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(BASE_URL + '/oauth/device/token', json=values, headers=headers)#.json()
    print(response)
    data = response.json()
    return data.get('access_token')"""
