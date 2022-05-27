import discord
import os
from neuralintents import GenericAssistant
from RoleReactClient import RoleReactClient

# Install neural stuff
import nltk
nltk.download('omw-1.4')

# Setup Chat bot
chatbot = GenericAssistant('intents.json')
chatbot.train_model()
chatbot.save_model()

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

# Actual Implementation
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("huhnbot"):
        response = chatbot.request(message.content[7:])
        await message.channel.send(response)


# Start Bot
client.run(token)