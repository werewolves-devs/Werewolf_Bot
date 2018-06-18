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

        member_ids = []
        for member in members:
            member_ids.append(member.id)
        message = creation_messages.cc_intro(
            member_ids)  # This is the message that will be sent to users once the channel is created

        # Role objects (based on ID)
        main_guild = self.bot.get_channel(bot_spam).guild
        roles = main_guild.roles
        game_master_role = discord.utils.find(lambda r: r.id == game_master, roles)
        dead_participant_role = discord.utils.find(lambda r: r.id == dead_participant, roles)
        frozen_participant_role = discord.utils.find(lambda r: r.id == frozen_participant, roles)
        default_permissions = {
            main_guild.default_role: discord.PermissionOverwrite(read_messages=False),
            frozen_participant_role: discord.PermissionOverwrite(send_messages=False),
            dead_participant_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
            game_master_role: discord.PermissionOverwrite(read_messages=True),  # Allow GM access
            self.bot.user: discord.PermissionOverwrite(read_messages=True),
            **{
                member: discord.PermissionOverwrite(read_messages=True) for member in members
            },
        }

        with open("conspiracy_channels/cc_data.json") as cc_data:
            try:
                data = json.load(cc_data)
            except JSONDecodeError:
                return await ctx.send('cc_data was not found or is invalid.')
        try:
            category = self.bot.get_channel(data['category_id'])
            if len(category.channels) > 49:
                # TODO: Category is full, make a new one
                pass
            else:
                # Use current category
                try:
                    channel = await ctx.guild.create_text_channel(
                        name,
                        category=category,
                        overwrites=default_permissions,
                        reason='Conspiracy Channel creation requested by ' + ctx.author.mention)
                    await channel.send(message)
                except Exception as e:
                    await ctx.channel.send('There was an error creating the channel, likely role finding. Please contact a Game Master for more info.\n\n*Game Masters: Check the console*')
                    raise e
        except Exception as e:
            # Category was invalid, create a new one now
            raise e

        with open("conspiracy_channels/cc_data.json", 'w') as cc_data:
            json.dump(data, cc_data)


def setup(bot):
    bot.add_cog(ConspiracyCog(bot))
