'''

                    ███████╗██╗  ██╗ ██████╗ ██████╗     ██████╗  ██████╗ ████████╗
                    ██╔════╝██║  ██║██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
                    ███████╗███████║██║   ██║██████╔╝    ██████╔╝██║   ██║   ██║
                    ╚════██║██╔══██║██║   ██║██╔═══╝     ██╔══██╗██║   ██║   ██║
                    ███████║██║  ██║╚██████╔╝██║         ██████╔╝╚██████╔╝   ██║
                    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═════╝  ╚═════╝    ╚═╝

                       - = https://github.com/werewolves-devs/werewolf_bot = -

'''

import discord
import asyncio
import random
import json
from emoji import emojize, demojize

# Import config data
import config

shops = []

class Shop():
    # This class holds both the shop's id (the message ID) and the shop's config (a JSON value)
    def __init__(self, message_id, config):
        self.message_id = message_id
        self.config = config

def find_shop_by_id(id):
    # Finds a shop config based on a shop (message) id
    for shop in shops:
        if shop.message_id == id:
            return shop.config
    return None

def get_shop_config():
    # Returns a json value with the default shop config file
    with open('shop.json') as f:
        return json.load(f) # Load shop config file

def is_shop(message_id):
    # returns True if 'message_id' is in the 'shops' list. Else returns false
    for shop in shops:
        if shop.message_id == message_id:
            return True
    return False

async def instantiate_shop(shop_config, channel, client):
    # Creates a new shop instance
    if shop_config == '':
        shop_config = get_shop_config() # If no config specified, use default
    embed = discord.Embed(title="Shop (Page 1/1)", description=shop_config["shop_description"], color=0x00ff00)
    for item in shop_config["items"]:
        embed.add_field(name="[{}] {}".format(item["emoji"], item["name"]), value="{} {}\n*{}*\n".format(item["price"], shop_config["currency"], item["description"]), inline=False) # Add Each item, in turn, to shop
    message = await channel.send(embed=embed)
    for item in shop_config["items"]:
        await message.add_reaction(emojize(item["emoji"], use_aliases=True)) # Add reactions to shop
    shops.append(Shop(message.id, shop_config)) # Add a new Shop() instance to the 'shops' list
    return message # Return the message so we can use it later

async def find_item_from_key(column, query, message_id):
    # Returns the item object based on 'column' from the shop associated with 'message_id' when it matches 'query'
    shop_config = find_shop_by_id(message_id)
    for item in shop_config["items"]:
        # print("Testing {} against {}".format(item[column], query)) # This is very useful when trying to find the full emoji name of something
        if item[column] == query:
            return item
