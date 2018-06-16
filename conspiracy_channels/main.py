import discord
from discord.ext import commands
import json
import story_time.cc_creation as creation_messages
from discord import Member

#TODO: Add auto-deletion of channels to reset, reset cc_data.json on reset
#TODO: Add season code to category name
#TODO: Add category number to category name
#TODO: Possibly move category ID to config?
#TODO: Configurable cc_data filename?

class ConspiracyCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True) # This means it is only called when no subcommand is
    async def cc(self, ctx):
        await ctx.send('CC Usage will go here')

    @cc.command(name='create')
    async def subcommand(self, ctx, name, *members: Member):
        #TODO: Randium needs to do database things to check if a user has correct privileges to add a user, create a channel, is abducted, etc etc, and other things.
        #TODO: Checks to ensure a correct number of users, plus other things
        message = creation_messages.cc_intro(members) # This is the message that will be sent to users once the channel is created
        data = {} # Our info from cc_data
        with open("conspiracy_channels/cc_data.json") as cc_data:
            data = json.load(cc_data)
        try:
            channels = self.bot.get_channel(data['category_id']).channels
            if len(channels) > 49:
                # Category is full, make a new one
            else:
                # Use current category
        except:
            # Category was invalid, create a new one now


def setup(bot):
    bot.add_cog(ConspiracyCog(bot))
