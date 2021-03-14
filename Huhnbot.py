# https://discord.com/oauth2/authorize?client_id=813038801211228201&scope=bot

import discord
import os

# stolen from https://github.com/Rapptz/discord.py/blob/master/examples/reaction_roles.py


class RoleReactClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ID of message that can be reacted to to add role
        self.role_message_id = 819957058719711232
        self.emoji_to_role = {
            # ID of role associated with partial emoji object 'spacehuhn_head' -> Huhn
            733382938657554555: 736544036151623690,
            # 804771444130840617: 818520356754292737  # ID of role associated with partial emoji object 'stonk' -> testBot
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


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    # list of unwanted profanities
    badWords = ["fuck", "shit", "nigg", "fag", "cunt", "sex"]
    noBadWord = True

    for word in badWords:
        if word in message.content.lower():
            await message.channel.send(str(message.author.mention) + " HEY, please keep it family friendly!")
            noBadWord = False
            break

    # only proceed if author didn't swear
    if noBadWord:
        if message.author == client.user:
            return

        elif client.user.mentioned_in(message) and ("shut up" in message.content):
            if discord.utils.find(lambda r: r.name == "Moderator", message.guild.roles) in message.author.roles:
                # ID for moderation channel
                await client.get_channel(733343988261584896).send("Huhnbot deactivated by " + str(message.author))
                exit()
            else:
                await message.channel.send("lol nope")

        # elif client.user.mentioned_in(message) and ("post" in message.content):
        #    if discord.utils.find(lambda r: r.name == "Moderator", message.guild.roles) in message.author.roles:
        #        await client.get_channel(733343036938911795).send(":warning: Click on the spacehuhn emoji below to become a server member, unlock all channels and connect with the community")  # ID for welcome channel

        elif client.user.mentioned_in(message) and ("hello" in message.content):
            await message.channel.send("hi :smile:")

        elif client.user.mentioned_in(message) and ("sus" in message.content):
            await message.channel.send(discord.utils.find(lambda r: r.name == "suspicious", message.guild.emojis))

        elif client.user.mentioned_in(message) and (("like waffles" in message.content) or ("love waffles" in message.content)):
            await message.channel.send("yes" + str(discord.utils.find(lambda r: r.name == "partyhuhn", message.guild.emojis)))

        elif client.user.mentioned_in(message) and ("bad bot" in message.content):
            await message.channel.send(":cry:")

        elif client.user.mentioned_in(message) and ("good bot" in message.content):
            await message.channel.send(":blush:")

        elif client.user.mentioned_in(message):
            await message.channel.send("Hmmm?")

token_path = 'token.txt'

if os.path.exists(token_path):
    with open(token_path, 'r') as file:
        token = file.read().replace('\n', '')
else:
    token = input("Discord Token:")
    with open(token_path, 'w') as file:
        file.write(token)

client.run(token)
