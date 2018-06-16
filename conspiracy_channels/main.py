import discord
from discord.ext import commands
import json
import story_time.cc_creation as creation_messages
from discord import Member
from config import game_master, participant, dead_participant, frozen_participant, bot_spam
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

        member_ids = []
        for member in members:
            member_ids.append(member.id)
        message = creation_messages.cc_intro(member_ids) # This is the message that will be sent to users once the channel is created


        #Role objects (based on ID)
        guild = self.bot.get_channel(bot_spam).guild
        roles = guild.roles
        game_master_role = discord.utils.find(lambda r: r.id == game_master, roles)
        participant_role = discord.utils.find(lambda r: r.id == participant, roles)
        dead_participant_role = discord.utils.find(lambda r: r.id == dead_participant, roles)
        frozen_participant_role = discord.utils.find(lambda r: r.id == frozen_participant, roles)
        ## Overwrites
        # Default for CC as soon as it's created: Bot has permissions, GMs have permissions, nobody else has permissions
        default_permissions = {
            self.bot.get_channel(bot_spam).guild.default_role: discord.PermissionOverwrite(read_messages=False), #Deny @everyone access
            participant_role:  discord.PermissionOverwrite(read_messages=False), #Deny @participant access
            dead_participant_role:  discord.PermissionOverwrite(read_messages=True, send_messages=False), #Allow dead access
            game_master_role:  discord.PermissionOverwrite(read_messages=True, send_messages=True), #Allow GM access
            self.bot.get_channel(bot_spam).guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True), #Allow bot access
        }


        with open("conspiracy_channels/cc_data.json") as cc_data:
            try:
                data = json.load(cc_data)
            except JSONDecodeError:
                await ctx.say('cc_data was not found or is invalid.')
            try:
                category = self.bot.get_channel(data['category_id'])
                if len(category.channels) > 49:
                    # Category is full, make a new one
                    pass
                else:
                    # Use current category
                    try:
                        channel = await ctx.channel.guild.create_text_channel(name, category=category, overwrites=default_permissions, reason='Conspiracy Channel creation requested by ' + str(ctx.message.author))
                        await channel.send(message)
                        #Now we set the permissions for each user:
                        for member in members:
                            await channel.set_permissions(member, reason='Initial CC Creation requested by ' + str(ctx.message.author), read_messages=True)


                    except Exception as e:
                        await ctx.channel.send('An error occured: ' + str(e))
            except Exception as e:
                # Category was invalid, create a new one now
                print(str(e))
                pass
            with open("conspiracy_channels/cc_data.json", 'w') as cc_data:
                json.dump(data, cc_data)


def setup(bot):
    bot.add_cog(ConspiracyCog(bot))
