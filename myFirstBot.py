import discord
import aiohttp
import urllib.request
import json
import time

#contents = urllib.request.urlopen("https://scratch.mit.edu/studios/5974533/").read()
#print(contents)

def projectDisplayText(contents):
	text = "**" + str(contents["title"]) + ' by ' + str(contents["author"]["username"]) + "**"
	text = text + "\n> :link: https://scratch.mit.edu/projects/" + str(contents["id"])
	text = text +  "\n:eye:" + str(contents["stats"]["views"])
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

	if(len(str(contents["instructions"])) > 0):
		desc = str(contents["instructions"])
		if(len(desc) > 300):
			desc = desc[:300] + "..."
		desc = desc.replace("```","\```",100)
		desc = desc.replace("`","\`",100)
		desc = desc.replace("**","\**",100)
		text = text + "\nInstructions: ```" + desc + "```"
	return text

def ordinalNumber(x):
    x = int(x)
    if (x < 0):
        return "-" + ordinalNumber(x * -1)
    elif x % 100 > 10 and x % 100 < 20:
        return str(x) + "th"
    elif x % 10 == 1:
        return str(x) + "st"
    elif x % 10 == 2:
        return str(x) + "nd"
    elif x % 10 == 3:
        return str(x) + "rd"
    else:
        return str(x) + "th"	

class MyClient(discord.Client):
    count = 0
    lastTime = time.time()
    
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        
    async def on_message(self, message):
        if(not message.author.bot):
            if(time.time() - self.lastTime >= 60):
                print("This bot was used",self.count,"time(s) in the last miniute")
                self.count = 0
                self.lastTime = time.time()
            commandArgs = message.content.split()
            try:
                if(commandArgs[0] == "!sh"):
                    if(commandArgs[1] == "project"):
                        projectid = "1"
                        try:
                            projectid = str(int(commandArgs[2]))
                        except ValueError:
                            print("Error: You have not enterned a valid project id.")
                                            
                        try:
                            contents = json.loads(urllib.request.urlopen("https://api.scratch.mit.edu/projects/" + projectid).read())
                            text = projectDisplayText(contents)
                            await message.channel.send(text)
                            self.count += 1
                        except urllib.error.HTTPError:
                            await message.channel.send("An error happened. maybe this project hasnt been shared yet or maybe it doesnt exist.")
                if(commandArgs[1] == "user"):
                    name = commandArgs[2]
                    if(len(commandArgs) > 3 and commandArgs[3] == "project"):
                        projects = int(str(urllib.request.urlopen("https://scratch.mit.edu/users/" + name + "/projects/").read()).split("Shared Projects (")[1].split(")")[0])
                        lookat = 0
                        if(commandArgs[4] == "latest"):
                            lookat = projects
                        else:
                            try:
                                lookat = str(int(commandArgs[4]))
                            except ValueError:
                                print("Error: You have not enterned a valid number.")
                        try:
                            contents = json.loads(urllib.request.urlopen("https://api.scratch.mit.edu/users/" + str(name) + "/projects?limit=1&offset=" + str(int(lookat) - 1) + "/").read())[0]
                            contents["author"]["username"] = name
                            text = "*" + name + "'s " + ordinalNumber(lookat) + " project*\n" + projectDisplayText(contents)
                            await message.channel.send(text)
                            self.count += 1
                        except urllib.error.HTTPError:
                            await message.channel.send("An error happened. this user doesnt exist.")
                    else:
                        try:
                            contents = json.loads(urllib.request.urlopen("https://api.scratch.mit.edu/users/" + name).read())
                            followers = int(str(urllib.request.urlopen("https://scratch.mit.edu/users/" + name + "/followers/").read()).split("Followers (")[1].split(")")[0])
                            projects = int(str(urllib.request.urlopen("https://scratch.mit.edu/users/" + name + "/projects/").read()).split("Shared Projects (")[1].split(")")[0])
							
                            text = 'Username: ' + str(contents["username"])
                            text = text + "\n> :link: https://scratch.mit.edu/users/" + name
                            text = text + "\n:earth_africa:" + str(contents["profile"]["country"])
                            text = text + "  :arrow_right:" + str(contents["history"]["joined"][:10])
                            text = text + "  :bust_in_silhouette:" + str(followers)
                            text = text + "\nShared Projects: " + str(projects)
                            text = text + "\nBio: ```" + str(contents["profile"]["bio"]) + "```"
                            text = text + "\nWhat I'm Working On: ```" + str(contents["profile"]["status"]) + "```"
                            await message.channel.send(text)
                            self.count += 1
                        except urllib.error.HTTPError:
                            await message.channel.send("An error happened. this user doesnt exist.")
                if(commandArgs[1] == "studio"):
                    studioid = "1"
                    try:
                        studioid = str(int(commandArgs[2]))
                    except ValueError:
                        print("Error: You have not enterned a valid studio id.")
                    if(len(commandArgs) > 3 and commandArgs[3] == "project"):
                        projects = int(str(urllib.request.urlopen("https://scratch.mit.edu/studios/" + studioid + "/projects/").read()).split("Shared Projects (")[1].split(")")[0])
                        lookat = 0
                        if(commandArgs[4] == "latest"):
                            lookat = projects
                        else:
                            try:
                                lookat = str(int(commandArgs[4]))
                            except ValueError:
                                print("Error: You have not enterned a valid number.")
                        try:
                            contents = json.loads(urllib.request.urlopen("https://api.scratch.mit.edu/studios/" + str(name) + "/projects?limit=1&offset=" + str(int(lookat) - 1) + "/").read())[0]
                            contents["author"]["username"] = name
                            text = "*" + ordinalNumber(lookat) + " project in studio " + string(studioid) + "*\n" + projectDisplayText(contents)
                            await message.channel.send(text)
                            self.count += 1
                        except urllib.error.HTTPError:
                            await message.channel.send("An error happened. this user doesnt exist.")          
                    else:          
                        try:
                            contents = json.loads(urllib.request.urlopen("https://api.scratch.mit.edu/studios/" + studioid).read()) 
                            
                            text = "**" + str(contents["title"]) + "**"
                            #text = text + "\nOnwer: " + contents[] for some reason the owner is in id form which isnt very useful
                            text = text + "\n> :link: https://scratch.mit.edu/studios/" + str(studioid)
                            text = text + "\n:bust_in_silhouette:" + str(contents["stats"]["followers"])
                            text = text + "\nCreated: " + str(contents["history"]["created"][:10])
                            text = text + "\nModified: " + str(contents["history"]["modified"][:10])
                            desc = contents["description"]
                            if(len(desc) > 600):
                                desc = desc.replace("```","\```",100)
                                desc = desc.replace("`","\`",100)
                                desc = desc.replace("**","\**",100)
                                desc = desc[:600] + "..."
                            if(len(desc) > 0):
                                text = text + "\nDescription: ```" + desc + "```"
                            sending = await message.channel.send(text)
                            await sending.add_reaction("💥")
                            self.count += 1
                        except urllib.error.HTTPError:
                            await message.channel.send("An error happened. maybe this studio doesnt exist.")
                except IndexError:
                    pass
				
            #print('Message from {0.author}: {0.content}'.format(message))
    async def on_reaction_add(self,reaction, user):
        pass
        #print(str(reaction.message.author))

client = MyClient(connector=aiohttp.TCPConnector(ssl=False))

f = open('secret.txt',"r")
data = json.load(f)
client.run(data["token"])
