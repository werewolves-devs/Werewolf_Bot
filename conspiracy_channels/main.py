import discord
from discord.ext import commands
import json
import story_time.cc_creation as creation_messages
from discord import Member
from json.decoder import JSONDecodeError

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
    async def cc_create(self, ctx, name, *members: Member):
        #TODO: Randium needs to do database things to check if a user has correct privileges to add a user, create a channel, is abducted, etc etc, and other things.
        #TODO: Checks to ensure a correct number of users, plus other things
        message = creation_messages.cc_intro(members) # This is the message that will be sent to users once the channel is created

        with open("conspiracy_channels/cc_data.json") as cc_data:
            try:
                data = json.load(cc_data)
            except JSONDecodeError:
                await ctx.say('cc-data was not found or is invalid.')
            try:
                category = self.bot.get_channel(data['category_id'])
                if len(category.channels) > 49:
                    # Category is full, make a new one
                    print("Making new category")
                    pass
                else:
                    # Use current category
                    print("Creating channel")
                    try:
                        await ctx.channel.guild.create_text_channel(name, category=category, reason='Conspiracy Channel creation requested by ' + str(ctx.message.author))
                    except Exception as e:
                        print(e)
            except:
                print("Category invalid")
                # Category was invalid, create a new one now
                pass
            with open("conspiracy_channels/cc_data.json", 'w') as cc_data:
                json.dump(data, cc_data)


def setup(bot):
    bot.add_cog(ConspiracyCog(bot))
