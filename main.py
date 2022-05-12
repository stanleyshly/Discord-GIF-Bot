import discord
import logging
import spacy
import json
import requests
import random
import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

client = discord.Client()
logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

#uncomment below to print log to console too
logging.getLogger().addHandler(logging.StreamHandler())
nlp = spacy.load(os.getenv("NLP_MODEL"))


# set the apikey and limit
apikey = os.getenv("TENOR_TOKEN")
max_gif_lmt = os.getenv("NUMBER_TENOR_SEARCH") # max gif to return


@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client)) 


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content: # this checks of message is sent
        if message.channel.name in os.getenv("WHITELIST_CHANNEL"):
            logging.info("Message Received at: "+ str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+  " Message is: " +  str(message.content))
            start_time =  time.time()    
            doc=nlp((message.content))
            noun_array = [chunk.text for chunk in doc.noun_chunks]
            verb_array =  [token.lemma_ for token in doc if token.pos_ == "VERB"]
            end_time = time.time()    
            logging.info("NLP Finished in: "+ str(end_time-start_time)+ " sec")
            search_term_big_array = verb_array + noun_array
            logging.info("All possible search terms are "+ str(search_term_big_array))
            start_time = end_time
            
            if search_term_big_array: # check if array is empty
                while True:
                    # our test search
                    search_term = search_term_big_array[random.randint(0,len(search_term_big_array)-1)]
                    logging.info("Search Term is: "+ search_term)
                    logging.info("Tenor Search Finished in: "+ str(end_time-start_time)+ " sec")
                    # get the top 8 GIFs for the search term
                    r = requests.get(
                        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, max_gif_lmt))
                    if r.status_code == 200:
                        # load the GIFs using the urls for the smaller GIF sizes
                        top_8gifs = json.loads(r.content)
                        if len(top_8gifs['results']) == 0:
                            logging.info("Tenor did not return any search terms")
                            await message.channel.send("https://c.tenor.com/pQJqTGuF-FIAAAAC/simply-delicious.gif") 
                            end_time = time.time()    
                            logging.info("GIF Send Finished in: "+ str(end_time-start_time)+ " sec")   
                            break 
                        if len(top_8gifs['results']) > 1:
                            random_gif_choice = random.randint(0,len(top_8gifs['results'])-1)
                        else:
                            random_gif_choice = 0
                        
                        gif_url = top_8gifs['results'][random_gif_choice]['media'][0]['gif']['url']
                        end_time = time.time()    
                        logging.info("Imjur Search Finished in: "+ str(end_time-start_time)+ " sec")
                        start_time = end_time
                        await message.channel.send(gif_url)
                        end_time = time.time()    
                        logging.info("GIF Send Finished in: "+ str(end_time-start_time)+ " sec")
                        break
                    break

            else:
                logging.info("NLP did not return any search terms")
                await message.channel.send("https://c.tenor.com/pQJqTGuF-FIAAAAC/simply-delicious.gif") 
                end_time = time.time()    
                logging.info("GIF Send Finished in: "+ str(end_time-start_time)+ " sec")




#discord API
client.run(os.getenv("DISCORD_TOKEN"))

