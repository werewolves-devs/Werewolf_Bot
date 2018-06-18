import json
from json.decoder import JSONDecodeError

import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import Context, Bot

import story_time.cc_creation as creation_messages
from config import game_master, dead_participant, frozen_participant, bot_spam


# TODO: Add auto-deletion of channels to reset, reset cc_data.json on reset
# TODO: Add season code to category name
# TODO: Add category number to category name
# TODO: Possibly move category ID to config?
# TODO: Configurable cc_data filename?

class ConspiracyCog:
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.group(invoke_without_command=True)  # This means it is only called when no subcommand is
    async def cc(self, ctx):
        await ctx.send('CC Usage will go here')

    @cc.command(name='create')
    async def cc_create(self, ctx: Context, name: str, *members: Member):
        # TODO: Randium needs to do database things to check if a user has correct privileges to add a user,
        # create a channel, is abducted, etc etc, and other things.
        # TODO: Checks to ensure a correct number of users,
        # plus other things

        if not ctx.message.author in members:
            members = members + (ctx.message.author,)

        member_ids = []
        for member in members:
            member_ids.append(member.id) # Create a list of member IDs to be sent to CC intro
        message = creation_messages.cc_intro(
            member_ids)  # This is the message that will be sent to users once the channel is created

        # Role objects (based on ID)
        main_guild = self.bot.get_channel(bot_spam).guild # Find the guild we're in
        roles = main_guild.roles # Roles from the guild
        game_master_role = discord.utils.find(lambda r: r.id == game_master, roles)                     # \
        dead_participant_role = discord.utils.find(lambda r: r.id == dead_participant, roles)           # | Find various role objects
        frozen_participant_role = discord.utils.find(lambda r: r.id == frozen_participant, roles)       # /
        default_permissions = {
            main_guild.default_role: discord.PermissionOverwrite(read_messages=False),                     # \
            frozen_participant_role: discord.PermissionOverwrite(send_messages=False),                     # |
            dead_participant_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),   # | Set the permissions for each role and the bot user
            game_master_role: discord.PermissionOverwrite(read_messages=True),                             # |
            self.bot.user: discord.PermissionOverwrite(read_messages=True),                                # /
            **{                                                                               # \
                member: discord.PermissionOverwrite(read_messages=True) for member in members # | Set permissions for each member
            },                                                                                # /
        }

        with open("conspiracy_channels/cc_data.json") as cc_data:
            try:
                data = json.load(cc_data) # Try to load conspiracy channel data from a file, ./cc_data.json
            except JSONDecodeError:
                return await ctx.send('cc_data was not found or is invalid.') # If we can't find it or it's invalid, throw an error
        try:
            category = self.bot.get_channel(data['category_id']) # Find the category based on the data from cc_data
        except:
            #Category couldn't be found, let's make a new one
            category = await main_guild.create_category('Conspiracy Channels', reason='Old CC Category not found; Creating new one') # TODO: Include season code etc
        if len(category.channels) > 49:
            # Current category is full, make a new one!
            category = await main_guild.create_category('Conspiracy Channels', reason='Old CC Category full; Creating new one') # TODO: Include season code etc
        try:
            try:
                channel = await ctx.guild.create_text_channel( # Create a text channel
                    name, # With the name 'name'
                    category=category, # In the category 'category' (A variable we just defined earlier)
                    overwrites=default_permissions, # Set the permissions to the 'default_permissions' object we created earlier
                    reason='Conspiracy Channel creation requested by ' + ctx.author.mention) # Set the reason for the Audit Log
                await channel.send(message) # Send our welcome message from cc_intro
            except Exception as e: # Catch any thrown exceptions and send an error to the user
                await ctx.channel.send('There was an error creating the channel, likely role finding. Please contact a Game Master for more info.\n\n*Game Masters: Check the console*')
                raise e # Send the full info to console
        except Exception as e:
            # Something went wrong. Let's tell the user.
            ctx.message.channel.send("Something went wrong. Please contact a Game Master for additional assistance.\n\n*Game Masters: Check the console*")
            raise e

        data['category_id'] = category.id
        with open("conspiracy_channels/cc_data.json", 'w') as cc_data:
            json.dump(data, cc_data) # Rewrite our 'data' back to disk, as it may have been modified


def setup(bot):
    bot.add_cog(ConspiracyCog(bot)) # Add cog to bot
