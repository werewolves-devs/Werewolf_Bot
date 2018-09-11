# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from discord import Embed

from config import max_cc_per_user, season, universal_prefix as unip, max_participants
from config import ghost_prefix as prefix
from interpretation import check
from main_classes import Mailbox
from management.db import isParticipant, personal_channel, db_get, db_set, signup, emoji_to_player, channel_get, \
    is_owner, get_channel_members
from management import db, dynamic as dy, general as gen, boxes as box
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
        
        if is_command(message,['success']):
            token = args[1]
            choice = args[2]

            if box.token_status(token) != 2:
                return []
            
        data = box.get_token_data(token)
        given_options = [int(data[3]),int(data[4]),int(data[5])]
    
        if choice not in given_options:
            return [Mailbox().respond("Invalid choice!",True).spam("A webhook has given an invalid bug. This means one of the following two things;\n1. There's bug;\n2. Someone's trying to hack the bots through a webhook.\n\nBoth are not good.")]

        box.add_choice(token,choice)
        return [Mailbox().respond("Got it! Thanks.\n*(Well, not really, this still needs to be done, but...)*")]

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

    if is_command(message, ['lead']):
        number = check.numbers(message)
        if not number:
            return [Mailbox().respond(gen.gain_leaderboard(user_id))]
        return [Mailbox().respond(gen.gain_leaderboard(user_id,max(number)))]
    if is_command(message, ['lead'], True):
        msg = "**Usage:** Gain a list of the most active users on the server.\n\n`" + prefix + "leaderboard <number>`\n\n"
        msg += "**Example:** `" + prefix + "lead 10`.\nThe number is optional, and doesn't have to be given."
    help_msg += "`" + prefix + "lead` - See an activity leaderboard."

    # Profile commands
    profile_commands = process_profile(message=message, is_game_master=isGameMaster, is_admin=isAdmin, is_peasant=isPeasant)
    if profile_commands:
        return profile_commands

    help_msg += "`" + prefix + "age` - Set your age\n"
    help_msg += "`" + prefix + "bio` - Set your bio\n"
    help_msg += "`" + prefix + "gender` - Set your gender\n"
    help_msg += "`" + prefix + "profile` - View a player's profile\n"

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
