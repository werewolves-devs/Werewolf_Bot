splash = '''

                    ███████╗██╗  ██╗ ██████╗ ██████╗     ██████╗  ██████╗ ████████╗
                    ██╔════╝██║  ██║██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
                    ███████╗███████║██║   ██║██████╔╝    ██████╔╝██║   ██║   ██║
                    ╚════██║██╔══██║██║   ██║██╔═══╝     ██╔══██╗██║   ██║   ██║
                    ███████║██║  ██║╚██████╔╝██║         ██████╔╝╚██████╔╝   ██║
                    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═════╝  ╚═════╝    ╚═╝

                       - = https://github.com/werewolves-devs/werewolf_bot = -

'''

splashes = [
'It\'s only selling your soul to the devil!',
'They\'re cheap, honest!'
]

import discord
import asyncio
import random
import json
from emoji import emojize, demojize

# Import config data
import config

shops = []

def get_shop_config():
    with open('shop.json') as f:
        return json.load(f) # Load shop config file

async def instantiate_shop(shop_config, channel, client):
    # Creates a new shop instance
    if shop_config == '':
        shop_config = get_shop_config() # If no config specified, use default
    embed = discord.Embed(title="Shop (Page 1/1)", description=shop_config["shop_description"], color=0x00ff00)
    for item in get_shop_config()["items"]:
        embed.add_field(name="[{}] {}".format(item["emoji"], item["name"]), value="{} {}\n*{}*\n".format(item["price"], shop_config["currency"], item["description"]), inline=False) # Add item to shop
    message = await channel.send(embed=embed)
    for item in shop_config["items"]:
        await message.add_reaction(emojize(item["emoji"], use_aliases=True)) # Add reactions to shop
    shops.append(message.id)
    return message # Return the message so we can use it later

async def find_item_from_key(column, query):
    with open('shop.json') as f:
        shop_config = json.load(f) # Load item file
    for item in get_shop_config()["items"]:
        # print("Testing {} against {}".format(item[column], query)) # This is very useful when trying to find the full emoji name of something
        if item[column] == query:
            return item
