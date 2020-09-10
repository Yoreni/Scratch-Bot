import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import aiohttp
import urllib.request
import json

#load_dotenv()
#theToken = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if(not message.author.bot):
            commandArgs = message.content.split()
            if(commandArgs[0] == "!sc"):
                if(commandArgs[1] == "project"):
                    projectid = "1"
                    try:
                        projectid = str(int(commandArgs[2]))
                    except ValueError:
                        print("Error: You have not enterned a valid project id.")
					
                    try:
                        contents = json.loads(urllib.request.urlopen("https://api.scratch.mit.edu/projects/" + projectid).read())
                        text = 'Author: ' + str(contents["author"]["username"])
                        text = text + "\nTitle: " + str(contents["title"])
                        text = text + "\nViews: " + str(contents["stats"]["views"])
                        text = text + "\nLoves: " + str(contents["stats"]["loves"])
                        text = text + "\nFavorites: " + str(contents["stats"]["favorites"])
                        text = text + "\nRemixes: " + str(contents["stats"]["remixes"])
                        text = text + "\nComments: " + str(contents["stats"]["comments"])
                        text = text + "\nLink: https://scratch.mit.edu/projects/" + str(projectid)
                        await message.channel.send(text)
                    except urllib.error.HTTPError:
                        await message.channel.send("An error happened. maybe this project hasnt been shared yet or maybe it doesnt exist.")
				
				
            #print('Message from {0.author}: {0.content}'.format(message))

client = MyClient(connector=aiohttp.TCPConnector(ssl=False))

f = open('secret.txt',"r")
data = json.load(f)
client.run(data["token"])









































