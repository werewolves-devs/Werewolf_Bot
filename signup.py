from config import prefix, game_stage
from management.main_manage import Mailbox, Game_Control

def signup(client,message):
    # TODO
    # A function needs to be created that checks the message.
    #
    # It should check that the variable game_stage is set to zero.
    if game_stage == 0:
        pass
        # The message must be checked on whether it has a vanilla emoji or not.
        # The function also needs to check if the user has already been signed up.
        # If all are the case, then sign the player up by using Game_Control.signup()
        # The function should return a Mailbox, in which a message is sent to the channel where the message was sent.
        #
        # If invalid, the Mailbox should contain an error message.
        # If valid, this function should sign up the user, then send a message to the channel that the user was signed up,
        #       and a message to the game_log that that user has signed up.
        #
        # Ask Randium or somebody else if you have any questions.
    else:
        return Mailbox().respond("You can't sign up when a game's running, sweetie. :kissing_heart:",message.channel)
