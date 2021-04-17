# Movies Bot
Chatbot for adding movies to your watchlist, built with Rasa.

## How to use this bot?

With this bot you can have an actual assistant that can add movies to your
watchlist. You can test it using the following
steps:

1. Train a Rasa model containing the Rasa NLU and Rasa Core models by running:
    ```
    rasa train
    ```
    The model will be stored in the `/models` directory as a zipped file.

2. Test the assistant by running:
    ```
    rasa run actions&
    rasa shell -m models --endpoints endpoints.yml
    ```
    This will load the assistant in your command line for you to chat.
