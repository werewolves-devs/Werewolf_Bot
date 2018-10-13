# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from discord import Embed

from config import max_cc_per_user, season, universal_prefix as unip, max_participants
from config import devil_prefix as prefix
from interpretation import check
from main_classes import Mailbox
from management.db import isParticipant, personal_channel, db_get, db_set, signup, emoji_to_player, channel_get, \
    is_owner, get_channel_members
from management.inventory import give_item, has_item
from roles_n_rules.item_usage import use_item
from management import db, dynamic as dy, general as gen, boxes as box, roulette, items, shop
from .profile import process_profile

PERMISSION_MSG = "Sorry, but you can't run that command! You need to have **{}** permissions to do that."
def todo():
    return [Mailbox().respond("I am terribly sorry! This command doesn't exist yet!", True)]

def is_command(message,commandtable,help=False):
    return check.is_command(message,commandtable,help,prefix)

def process(message, isGameMaster=False, isAdmin=False, isPeasant=False):
    user_id = message.author.id
    message_channel = message.channel.id

    help_msg = "**List of commands:**\n"

    args = message.content.split(' ')

    # =============================================================
    #
    #                         BOT COMMANDS
    #
    # =============================================================
    if isPeasant == True:
        pass

    # =============================================================
    #
    #                         ADMINISTRATOR
    #
    # =============================================================
    if isAdmin == True:
        help_msg += "\n __Admin commands:__\n"

    elif is_command(message, ['delete_category','start']):
        return [Mailbox().respond(PERMISSION_MSG.format("Administrator"), True)]


    # =============================================================
    #
    #                         GAME MASTERS
    #
    # =============================================================
    if isGameMaster == True:
        help_msg += "\n__Game Master commands:__\n"

        if is_command(message, ['userinv','userinventory']):
            target = check.users(message)
            if not target:
                return [Mailbox().respond("**INVALID SYNTAX:**\nNo target provided!",True)]

            answer = Mailbox().spam("**__<@{}>'S BALANCE__**".format(target[0]))

            for item in items.jget("items"):
                if has_item(target[0],item["code"]):
                    answer.spam_add('\n{}x - **'.format(has_item(target[0],item["code"],False)) + item["name"] + '**')
            return [answer]
        if is_command(message, ['userinv','userinventory'], True):
            return todo()
        help_msg += "`" + prefix + "userinv` - View a user's inventory.\n"

    elif is_command(message, []):
        return [Mailbox().respond(PERMISSION_MSG.format("Game Master"), True)]

    # =============================================================
    #
    #                         PARTICIPANTS
    #
    # =============================================================

    if isParticipant(user_id):
        help_msg += "\n__Participant commands:__\n"

        user_undead = int(db_get(user_id,'undead'))

    elif is_command(message, []):
        return [Mailbox().respond(PERMISSION_MSG.format("Participant"), True)]


    # =============================================================
    #
    #                         EVERYONE
    #
    # =============================================================

    help_msg += '\n\n'

    '''inventory'''
    if is_command(message, ['inv','inventory','bal','balance']):
        answer = Mailbox().dm("**__YOUR CURRENT BALANCE__**",user_id)
        for item in items.jget("items"):
            if has_item(user_id,item["code"]):
                answer.dm_add('\n{}x - **'.format(has_item(user_id,item["code"],False)) + item["name"] + '**')
        return [answer]
    if is_command(message, ['inv','inventory','bal','balance'], True):
        return todo()
    help_msg += "`" + prefix + "inventory` - View your inventory.\n"

    '''shop'''
    if is_command(message, ['shop']):
        answer = Mailbox()

        for msg in shop.get_market_message():
            answer.respond(msg,True)
        
        return answer
    if is_command(message, ['shop']):
        msg = "**Usage:** View the Devil Bot's shop.\n\n`" + prefix + "shop`"
        return [Mailbox().respond(msg,True)]
    help_msg += "`" + prefix + "shop` - View the Devil's shop."

    help_msg += "\n\n__Item specific commands:__"

    '''attack'''
    if is_command(message, ['attack', 'dagger', 'kill']):
        pass # TODO

    '''disguise'''
    if is_command(message,['disguise','dis']):
        return [use_item(103,message)]
    if is_command(message,['disguise','dis'],True):
        msg = "**Usage:** Disguise a participant.\n\n`" + prefix + "disguise @Randium#6521 Innocent`\n\n"
        msg += "This command can only be used by participants. You can disguise yourself."
        return [Mailbox().respond(msg,True)]
    help_msg += "`" + prefix + "disguise` - Disguise a participant.\n"

    '''hide'''
    if is_command(message,['hide']):
        return [use_item(100,message)]
    if is_command(message,['disguise','dis'],True):
        msg = "**Usage:** Disguise a participant.\n\n`" + prefix + "disguise @Randium#6521 Innocent`\n\n"
        msg += "This command can only be used by participants. You can disguise yourself."
        return [Mailbox().respond(msg,True)]
    help_msg += "`" + prefix + "hide` - Become invisible for the night.\n"

    # --------------------------------------------------------------
    #                          HELP
    # --------------------------------------------------------------
    help_msg += "\n\n*If you have any more questions, feel free to ask any of the Game Masters!*"

    '''help'''
    if is_command(message,['help']) and is_command(message,['help'],True) == False:
        return [Mailbox().respond(help_msg,True)]
    if is_command(message,['help'],True):
        answer = Mailbox().respond("Hey there! `" + prefix + "help` will give you a list of commands that you can use.")
        answer.respond_add("\nIf you have any questions, feel free to ask any of the Game Masters!")
        return [answer]

    if message.content.startswith(prefix):
        return [Mailbox().respond("Sorry bud, couldn't find what you were looking for.", True)]

    return []
