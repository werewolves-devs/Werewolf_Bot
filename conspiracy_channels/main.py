import discord
from discord.ext import commands
import json
import story_time.cc_creation as creation_messages


#TODO: Add auto-deletion of channels to reset, reset cc_data.json on reset
#TODO: Add season code to category name
#TODO: Add category number to category name
#TODO: Possibly move category ID to config?
#TODO: Configurable cc_data filename?


def create_channel(client, members):
    '''This function expects a list of discord IDs, such as [457261890289008641, 457254721388806147]'''
    #TODO: Randium needs to do database things to check if a user has correct privileges to add a user, create a channel, is abducted, etc etc, and other things.
    #TODO: Checks to ensure a correct number of users, plus other things
    message = creation_messages.cc_intro(members) # This is the message that will be sent to users once the channel is created
    data = {} # Our info from cc_data
    with open("conspiracy_channels/cc_data.json") as cc_data:
        data = json.load(cc_data)
    try:
        channels = client.get_channel(data['category_id']).channels
        print(channels)
    except:
        print(client.get_channel(data['category_id']))               #None of these work (They think the channel doesn't exist)
        print(client.get_channel(4572648103635845130))               #None of these work
        print(client.get_channel('4572648103635845130'))             #None of these work
        print("Either category doesn't exist or it's empty")         #None of these work

class ConspiracyCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cc', aliases=['c'])
    async def cc(self, ctx, command, member: discord.Member):
        if command == 'create':
            #TODO: Randium needs to do database things to check if a user has correct privileges to add a user, create a channel, is abducted, etc etc, and other things.
            #TODO: Checks to ensure a correct number of users, plus other things
            message = creation_messages.cc_intro(members) # This is the message that will be sent to users once the channel is created
            data = {} # Our info from cc_data
            with open("conspiracy_channels/cc_data.json") as cc_data:
                data = json.load(cc_data)
            try:
                channels = self.bot.get_channel(data['category_id']).channels
                print(channels)
            except:
                print(self.bot.get_channel(data['category_id']))               #None of these work (They think the channel doesn't exist)
                print(self.bot.get_channel(4572648103635845130))               #None of these work
                print(self.bot.get_channel('4572648103635845130'))             #None of these work
                print("Either category doesn't exist or it's empty")           #None of these work
            else:
                print(command)

def setup(bot):
    bot.add_cog(ConspiracyCog(bot))
