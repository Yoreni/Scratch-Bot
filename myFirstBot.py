import discord
import aiohttp
import urllib.request
import json

#contents = urllib.request.urlopen("https://scratch.mit.edu/users/yoreni/projects/").read()
#print(contents)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if(not message.author.bot):
            commandArgs = message.content.split()
            if(commandArgs[0] == "sh!"):
                if(commandArgs[1] == "project"):
                    projectid = "1"
                    try:
                        projectid = str(int(commandArgs[2]))
                    except ValueError:
                        print("Error: You have not enterned a valid project id.")
					
                    try:
                        contents = json.loads(urllib.request.urlopen("https://api.scratch.mit.edu/projects/" + projectid).read())
                        text = "**" + str(contents["title"]) + ' by ' + str(contents["author"]["username"]) + "**"
                        text = text + "\n> :link: https://scratch.mit.edu/projects/" + str(projectid)
                        text = text + "\n:eye:" + str(contents["stats"]["views"])
                        text = text + "  :heart:" + str(contents["stats"]["loves"])
                        text = text + "  :star: " + str(contents["stats"]["favorites"])
                        text = text + "  :cyclone: " + str(contents["stats"]["remixes"])
                        text = text + "  :speech_left: " + str(contents["stats"]["comments"])
                        
                        if (len(str(contents["description"])) > 0):
                            desc = str(contents["description"])
                            if(len(desc) > 300):
                                desc = desc[:300] + "..."
                            desc = desc.replace("```","\```",100)
                            desc = desc.replace("`","\`",100)
                            desc = desc.replace("**","\**",100)
                            text = text + "\nNotes and Credits: ```" + desc + "```"
                        if (len(str(contents["instructions"])) > 0):
                            desc = str(contents["instructions"])
                            if(len(desc) > 300):
                                desc = desc[:300] + "..."
                            desc = desc.replace("```","\```",100)
                            desc = desc.replace("`","\`",100)
                            desc = desc.replace("**","\**",100)
                            text = text + "\nInstructions: ```" + desc + "```"
                        await message.channel.send(text)
                    except urllib.error.HTTPError:
                        await message.channel.send("An error happened. maybe this project hasnt been shared yet or maybe it doesnt exist.")
            if(commandArgs[1] == "user"):
                name = commandArgs[2]
                try:
                    contents = json.loads(urllib.request.urlopen("https://api.scratch.mit.edu/users/" + name).read())
                    #followers = int(str(urllib.request.urlopen("https://scratch.mit.edu/users/" + name + "/followers/").read()).split("Followers (")[1].split(")")[0])
                    #projects = int(str(urllib.request.urlopen("https://scratch.mit.edu/users/" + name + "/projects/").read()).split("Shared Projects (")[1].split(")")[0])
                    
                    text = 'Username: ' + str(contents["username"])
                    text = text + "\nLocation: " + str(contents["profile"]["country"])
                    text = text + "\nJoin Date: " + str(contents["history"]["joined"][:10])
                    #text = text + "\nFollowers: " + str(followers)
                    #text = text + "\nShared Projects: " + str(projects)
                    text = text + "\nBio: " + str(contents["profile"]["bio"])
                    text = text + "\nWhat I'm Working On: " + str(contents["profile"]["status"])
                    text = text + "\nLink: https://scratch.mit.edu/users/" + str(name)
                    await message.channel.send(text)
                except urllib.error.HTTPError:
                    await message.channel.send("An error happened. this user doesnt exist.")
				
            #print('Message from {0.author}: {0.content}'.format(message))

client = MyClient(connector=aiohttp.TCPConnector(ssl=False))

f = open('secret.txt',"r")
data = json.load(f)
client.run(data["token"])
