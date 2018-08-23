# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from discord import Embed

import interpretation.check as check
import roles_n_rules.functions as func
from config import max_cc_per_user, season, universal_prefix as unip
from config import ghost_prefix as prefix
from interpretation.check import is_command as old_is_command
from main_classes import Mailbox
from management.position import valid_distribution
from management.db import isParticipant, personal_channel, db_get, db_set, signup, emoji_to_player, channel_get, \
    is_owner, get_channel_members
from story_time.commands import cc_goodbye, cc_welcome
import story_time.eastereggs as eggs

PERMISSION_MSG = "Sorry, but you can't run that command! You need to have **{}** permissions to do that."

def todo():
    return [Mailbox().respond("I am terribly sorry! This command doesn't exist yet!", True)]

def is_command(message,list,bool=False,std_prefix=prefix):
    return old_is_command(message,list,bool,std_prefix)


def process(message, isGameMaster=False, isAdmin=False, isPeasant=False):
    user_id = message.author.id
    message_channel = message.channel.id

    help_msg = "**List of commands:**\n"

    # =============================================================
    #
    #                         BOT COMMANDS
    #
    # =============================================================
    if isPeasant == True:
        if is_command(message,['kill'],False,unip):
            answer = Mailbox()
            for member in message.mentions:
                answer.dm("Hey there, buddy!\n",member.id)
                answer.dm_add("I\'m sorry for you that you died, that you lost the game! ")
                answer.dm_add("But don't worry, there\'s still a lot to do in the afterlife!\n")
                answer.dm_add("This story isn\'t finished, but it does need more explanation.")

    # =============================================================
    #
    #                         ADMINISTRATOR
    #
    # =============================================================
    if isAdmin == True:
        help_msg += "\n __Admin commands:__\n"

    elif is_command(message, ['delete_category']):
        return [Mailbox().respond(PERMISSION_MSG.format("Administrator"), True)]

    # =============================================================
    #
    #                         GAME MASTERS
    #
    # =============================================================
    if isGameMaster == True:
        help_msg += "\n__Game Master commands:__\n"

    elif is_command(message, ['addrole','assign','day','night','open_signup','whois']):
        return [Mailbox().respond(PERMISSION_MSG.format("Game Master"), True)]

    # =============================================================
    #
    #                         DEAD PARTICIPANTS
    #
    # =============================================================

    if not isParticipant(user_id):
        help_msg += "\n__Participant commands:__\n"

        user_undead = int(db_get(user_id,'undead'))

    # =============================================================
    #
    #                         EVERYONE
    #
    # =============================================================

    help_msg += '\n\n'

    '''age'''
    # Allows users to set their age.
    if is_command(message, ['age']):
        # TODO
        return todo()
    if is_command(message, ['age'], True):
        msg = "**USAGE:** This command is used to set your age. \n\n`" + prefix + "age<number>\n\n**Example:** `!age 19`"
        return [Mailbox().respond(msg,True)]
    help_msg += "`" + prefix + "age` - Set your age.\n"

    '''profile'''
    # This command allows one to view their own profile
    # When giving another player's name, view that player's profile
    if is_command(message, ['profile']):
        # TODO
        return todo()
    if is_command(message, ['profile'], True):
        msg = "**USAGE:** The use of this command is to check your own profile, you can check other peoples profiles by adding their name. \n\n`" + prefix + "profile <user>`\n\n**Example:** `!profile @Randium#6521`"
        return [Mailbox().respond(msg,True)]
    help_msg += "`" + prefix + "profile` - See a player's profile.\n"

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
