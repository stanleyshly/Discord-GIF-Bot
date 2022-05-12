# Pranav Bot

This is a Discord bot that sends semi-relavent gifs to "spice" up your server discussions just a bit more. 

Inspired by Pranav, of course

## Setup
1) Install dependencies with ``` pip install -r requirements.txt ```
2) Create ``` .env ``` file in the same directory
3) Set up ```.env``` to look something like this:
```
DISCORD_TOKEN=DISCORDTOKENGOESHERE
TENOR_TOKEN=TENORTOKENGOESHERE
WHITELIST_CHANNEL=["stanley-bot-playground"]
NUMBER_TENOR_SEARCH=8
NLP_MODEL=en_core_web_trf
```
4) Add Discord and Tenor token 
5) Create array with all channels where bot will reply with GIFs (Warning, Failure to do so correctly) will result in very annoyed ex-friends.
6) Set ```NUMBER_IMGUR_SEARCH``` to set the max of gifs to search on Imgur each time(increasing this number slows down the bot significantly but allows for a greater variety of GIFs returned)
7) Set  ```NLP_MODEL``` to use a model that Spacey supports; install and configure the models with instructions here before starting the bot: [Spacy Website](https://spacy.io/models)
7a) For english, ```en_core_web_trf``` is alright, but if compute limited, use ```en_core_web_sm```
8) Start bot and enjoy