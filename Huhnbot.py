# https://discord.com/oauth2/authorize?client_id=813038801211228201&scope=bot

import discord
import os
import subprocess
import sys
from random import randint

from discord import message


class RoleReactClient(discord.Client):
    # stolen from https://github.com/Rapptz/discord.py/blob/master/examples/reaction_roles.py
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ID of message that can be reacted to to add role
        self.role_message_id = 819957058719711232
        self.emoji_to_role = {
            733382938657554555: 736544036151623690,
            # ID of role associated with partial emoji object 'spacehuhn_head' -> Huhn

            # 804771444130840617: 818520356754292737
            # ID of role associated with partial emoji object 'stonk' -> testBot
        }

    async def on_raw_reaction_add(self, payload):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            # print(payload.emoji.id)
            role_id = self.emoji_to_role[payload.emoji.id]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally add the role
            await payload.member.add_roles(role)
            print(str(role) + " given to " + str(payload.member.name))
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji.id]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            # Makes sure the member still exists and is valid
            return

        try:
            # Finally, remove the role
            await member.remove_roles(role)
            print(str(role) + " removed from " + str(member.name))
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass


# This bot requires the members and reactions intents.
intents = discord.Intents.default()
intents.members = True
client = RoleReactClient(intents=intents)
lastMessage = None


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global lastMessage
    # list of unwanted profanities
    badWords = ["fuck", "shit", "nigg", "fag", "cunt"]
    noBadWord = True
    reacted = False
    msg = message.content.lower()
    pinged = client.user.mentioned_in(message)
    reactionTriggers = {
        "hello": "hi :smile:",
        "good morning": "moin",
        "good day": ":blush:",
        "good evening": "good evening to you too :grinning:",
        "good night": "good night :yawning_face:",
        "sus": str(discord.utils.find(lambda r: r.name == "suspicious", client.get_guild(724901805607223336).emojis)),
        "like waffles": "yes" + str(discord.utils.find(lambda r: r.name == "partyhuhn", client.get_guild(724901805607223336).emojis)),
        "love waffles": "yes" + str(discord.utils.find(lambda r: r.name == "partyhuhn", client.get_guild(724901805607223336).emojis)),
        "bad bot": ":cry:",
        "good bot": ":blush:",
        "help": "Sorry but I can't help you with that yet. Post your problem in the related help channel instead.",
        "die": "not today",
        "seppuku": "not today",
        "harakiri": "not today",
        "kill": "not today",
        "space chicken": str(discord.utils.find(lambda r: r.name == "spacehuhn", client.get_guild(724901805607223336).emojis)),
        "deauther": "you can download the latest version here: https://github.com/SpacehuhnTech/esp8266_deauther/releases",
        "chicken nugget": "you monster :fearful:",
        "taste": "oh no :fearful:"
    }

    # spam filtering
    if lastMessage and (message.content == lastMessage.content) and (message.author == lastMessage.author) and (message.channel == lastMessage.channel) and not message.author.bot:
        try:
            await message.author.send("Hi. I've deleted your latest message because it was identical to the message sent before it.")
        except Exception:
            pass
        finally:
            await message.delete()
        return
    lastMessage = message

    for word in badWords:
        if word in msg:
            await message.channel.send(str(message.author.mention) + "HEY, please keep it family friendly!")
            noBadWord = False
            break

    if noBadWord:
        # only proceed if author didn't swear
        if message.author == client.user:
            return

        if (str(client.user.name).lower() in msg) or pinged:
            # proceed if bot is mentioned
            for key in reactionTriggers:
                if key in msg:
                    await message.channel.send(reactionTriggers[key])
                    reacted = True
                    break

        if pinged and not reacted:
            # only proceed if bot is directly adressed
            if "shut up" in msg:
                if discord.utils.find(lambda r: r.name == "Moderator", message.guild.roles) in message.author.roles:
                    # ID for moderation channel
                    await client.get_channel(733343988261584896).send("Huhnbot deactivated by " + str(message.author))
                    exit()
                else:
                    await message.channel.send("lol nope")
                    return

            elif "update" in msg:
                if discord.utils.find(lambda r: r.name == "Moderator", message.guild.roles) in message.author.roles:
                    try:
                        process = subprocess.Popen(
                            ["git", "pull"], stdout=subprocess.PIPE)
                        output = process.communicate()[0].decode("utf-8")
                    except:
                        print("git pull not working :(")
                    await message.channel.send(f"Huhnbot updated by {message.author} ```{output}```")
                    os.execv(sys.executable, ['python'] + sys.argv)
                else:
                    await message.channel.send("lol nope")
                    return

            elif "meaning of life" in msg:
                await message.channel.send('According to Deep Thought (and Google) the  Answer to the Ultimate Question of Life, the Universe, and Everything is "42".')
                return

            elif "play a game" in msg:
                await message.channel.send("Here you go: https://github.com/skickar/ChickenManGame")
                return

            elif "i have a question" in msg:
                temp = randint(0, 6)
                if temp == 0:
                    await message.channel.send("yes")
                elif temp == 1:
                    await message.channel.send("probably")
                elif temp == 2:
                    await message.channel.send("could be")
                elif temp == 3:
                    await message.channel.send("maybe")
                elif temp == 4:
                    await message.channel.send("I don't think so")
                elif temp == 5:
                    await message.channel.send("probably not")
                elif temp == 6:
                    await message.channel.send("no")
                else:
                    await message.channel.send("I'm not sure")
                return

            else:
                await message.channel.send("Hmmm?")
                return

token_path = 'token.txt'

if os.path.exists(token_path):
    with open(token_path, 'r') as file:
        token = file.read().replace('\n', '')
else:
    token = input("Discord Token:")
    with open(token_path, 'w') as file:
        file.write(token)

client.run(token)
