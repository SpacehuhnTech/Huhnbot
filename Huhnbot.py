import discord
import os
import subprocess
import sys
from neuralintents import GenericAssistant

MODEL_NAME = 'huhn'

# Setup Chat bot
chatbot = GenericAssistant('intents.json', model_name=MODEL_NAME)

def buildModel():
    chatbot.train_model()
    chatbot.save_model()

try:
    chatbot.load_model(MODEL_NAME)
except:
    buildModel()

if len(sys.argv) > 1 and sys.argv[1] == '-debug':
    buildModel()

# Load Discord API Token from file
def loadToken():
    TOKEN_PATH = 'token.txt'
    token = ''

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as file:
            token = file.read().replace('\n', '')
    # (if file doesn't exist, ask for it via standard input, and save it)
    else:
        token = input("Discord Token:")
        with open(TOKEN_PATH, 'w') as file:
            file.write(token)
    
    return token

# This bot requires the members and reactions intents.
#intents = discord.Intents.default()
#intents.members = True
client = discord.Client()#intents=intents)

# On Startup
@client.event
async def on_ready():
    message = "[Started] Logged in as {0.user}".format(client)
    print(message)

    if len(sys.argv) == 1 or sys.argv[1] != '-debug':
        channel = client.get_channel(817402120063549451)
        await channel.send(message)

# Helper functions
def fromMod(message):
    is_admin = message.author.top_role.permissions.administrator
    #is_admin = discord.utils.find(lambda r: r.name == "Admin", message.guild.roles) in message.author.roles
    is_mod = discord.utils.find(lambda r: r.name == "Moderator", message.guild.roles) in message.author.roles

    return is_admin or is_mod

# On Message
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # [===== Message to Huhnbot =====] #
    if "huhnbot" in message.content.lower() or client.user.mentioned_in(message):
        send_as_reply = False
        message_content = message.content
        
        # Reply to earlier message
        if message.reference is not None:
            pinged_message = message
            ref_message = await message.channel.fetch_message(message.reference.message_id)

            # Update message to use referenced message
            message = ref_message
            send_as_reply = True
            
            # When pinged only with "huhnbot", react on original message
            if message_content.lower() == "huhnbot" or not fromMod(pinged_message):
                message_content = ref_message.content
            
            # Delete message where huhnbot was pinged
            await pinged_message.delete()

        response = chatbot.request(message_content)

        if send_as_reply:
            await message.reply(response)
        else:
            await message.channel.send(response)

        return

    # [===== Debug =====] #
    if message.content.startswith("huhndebug "):
        if not fromMod(message):
            await message.channel.send(f"Hahahah. Nope!")
            return

        cmd = message.content[10:]
        # [UPDATE]
        if cmd == 'update':
            try:
                process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
                output = process.communicate()[0].decode("utf-8")
                await message.channel.send(f"Huhnbot updated by {message.author} ```{output}```")
            except Exception as e:
                await message.channel.send(f"git pull not working :frowning: ```{e}```")
                print("git pull not working :(")
        # [RESTART]
        elif cmd == 'restart':
            os.execv(sys.executable, ['python3'] + sys.argv)
        # [BUILD]
        elif cmd == 'build':
            await message.channel.send(f"Rebuilding... :rocket:")
            buildModel()
            await message.channel.send(f"Done :slight_smile:")
            print("Finished rebuilding model")
        # [404]
        else:
            await message.channel.send(f"Don't know '{cmd}'")
           
# Start Bot
client.run(loadToken())