import discord
import os
import subprocess
import sys
from neuralintents import GenericAssistant
from RoleReactClient import RoleReactClient

# Install neural stuff
#import nltk
#nltk.download('omw-1.4')

# Setup Chat bot
chatbot = GenericAssistant('intents.json')
#chatbot.train_model()
#chatbot.save_model()
chatbot.load_model('assistant_model')

# Load Discord API Token from file
# (if file doesn't exist, ask for it via standard input, and save it)
TOKEN_PATH = 'token.txt'

if os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, 'r') as file:
        token = file.read().replace('\n', '')
else:
    token = input("Discord Token:")
    with open(TOKEN_PATH, 'w') as file:
        file.write(token)

# This bot requires the members and reactions intents.
intents = discord.Intents.default()
intents.members = True
client = RoleReactClient(intents=intents)

# On Startup
@client.event
async def on_ready():
    message = "[Started] Logged in as {0.user}".format(client)
    print(message)

    if sys.argv[1] != '-debug':
        channel = client.get_channel(817402120063549451)
        await channel.send(message)

# Helper functions
def fromMod(message):
    return message.author.top_role.permissions.administrator

# On Message
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("huhnbot "):
        response = chatbot.request(message.content[8:])
        await message.channel.send(response)

    if message.content.startswith("/huhnbot "):
        if not fromMod(message):
            await message.channel.send(f"You shall not pass!")
            return

        cmd = message.content[9:]
        # ===== UPDATE ===== #
        if cmd == 'update':
            try:
                process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
                output = process.communicate()[0].decode("utf-8")
                await message.channel.send(f"Huhnbot updated by {message.author} ```{output}```")
            except Exception as e:
                await message.channel.send(f"git pull not working :( ```{e}```")
                print("git pull not working :(")
        # ===== RESTART ===== #
        elif cmd == 'restart':
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            await message.channel.send(f"Don't know '{cmd}'")
           
# Start Bot
client.run(token)