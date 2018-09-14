from management.general import update_roulette_score
from main_classes import Mailbox
import config
import random
import time

class Ruser:
    def __init__(self,user_class,alive=True):
        self.user = user_class
        self.victims = []
        self.alive = alive
        self.score = 0
    
    def kill(self,victim):
        self.victims.append(victim)
        victim.alive = False
        self.score += 2
        update_roulette_score(self.user.id,self.score)
        return self
    
    def __str__(self,recursive='\n'):

        failure = '|'
        next = '|            '
        success = '|---> '
        skull = '💀 '

        answer = recursive + failure + recursive + success
        if not self.alive:
            answer += skull
        answer += '**{}**'.format(self.user.display_name)

        for victim in self.victims:
            answer += victim.__str__(recursive+next)
        return answer

deadies = []
winners = []

challenger = None
acceptant = None
game_channel = None

bullet_number = 0
bullet = 0
timeout = 0

def is_playing(user):
    global challenger
    global acceptant

    if user in [challenger,acceptant]:
        return True
    return False

def take_shot(message):
    global deadies
    global winners
    global challenger
    global acceptant
    global game_channel
    global bullet_number
    global bullet
    global timeout

    user = message.author
    channel = message.channel

    # Start a game.
    if challenger == None:
        for deadie in deadies:
            if deadie.user == user:
                return [Mailbox().respond("Sorry, bud. Ya can't play if you're dead.",True)]
        challenger = user
        game_channel = channel
        timeout = time.time()
        return Mailbox().respond("<@{}> has grabbed the pistol and loaded a bullet in it! Who wants to play a dangerous game?".format(user.id))

    # Redirect wrong channel
    if game_channel != channel:
        return Mailbox().respond("I'm sorry! There's currently a game going on in <#{}>, go check it out!".format(game_channel.id),True)

    # Do not play game with yourself
    if acceptant == None and user == challenger:
        return Mailbox().respond("Not so fast! Wait for someone to accept your challenge!")

    # Accept a challenged game
    if acceptant == None and user != challenger:
        for deadie in deadies:
            if deadie.user == user:
                return [Mailbox().respond("Sorry, bud. Ya can't play if you're dead.",True)]
        acceptant = user
        timeout = time.time()
        bullet = random.randint(1,6)
        bullet_number = 0
        return Mailbox().respond("You take the pistol, give it a turn, then hand the pistol over to <@{}>! They will start!".format(challenger.id))

    # Ignore non-participating players
    if user not in [challenger,acceptant]:
        for deadie in deadies:
            if deadie.user == user:
                return [Mailbox().respond("You attempted to grab the pistol, but then you realised you were already dead!",True)]
        return Mailbox().respond("The pistol was out of your reach. You failed to grab it.",True)
    
    # Hold the other from shooting twice.
    if user == acceptant:
        return Mailbox().respond("It\'s not your turn! Wait for <@{}> to finish.".format(challenger.id))
    
    # Let the user shoot
    if user == challenger:
        bullet_number += 1
        if bullet == bullet_number:
            user = None
            victim = None

            for player in winners:
                if player.user == acceptant:
                    user = player
                if player.user == challenger:
                    victim = player
                    winners.remove(victim)

            if victim == None:
                victim = Ruser(challenger)
            if user == None:
                user = Ruser(acceptant)
                winners.append(user)
            user.kill(victim)
            deadies.append(victim)
            
            answer = Mailbox().respond("You pull the trigger, and your brains get splattered all over the place.",False,['💀'])
            answer.respond("**{} WINS!**".format(user.display_name))

            challenger = None
            acceptant = None
            game_channel = None

            bullet_number = 0
            bullet = 0
            timeout = 0

            return answer
        
        switch = challenger
        challenger = acceptant
        acceptant = switch
        timeout = time.time()
        return Mailbox().respond("You pull the trigger, and you hear a small **CLICK!** It's <@{}>'s turn now.".format(challenger.id))
    
    return Mailbox().spam("I got a strange event during the Russian Roulette! Can somebody check this out?").respond("**ERROR:** Invalid if-statwments. Please report this to the Game Masters!")

def surrender(need_for_check=True,user=None):
    global deadies
    global winners
    global challenger
    global acceptant
    global game_channel
    global bullet_number
    global bullet
    global timeout

    if challenger == None:
        return Mailbox()
    
    if user != None and user != challenger:
        return Mailbox()

    if acceptant == None:
        game_channel = None
        if user == None:
            if time.time() - timeout > 600:
                answer = Mailbox().respond("It has taken too long for anyone to accept your challenge, <@{}>! If you're still here, please rejoin the challenge.".format(challenger.id))
                challenger = None
                return answer
            return Mailbox()
        challenger = None
        return Mailbox().respond("<@{}> fired the round in the air, and put down the gun. Let's play this game later!".format(user.display_name))

    if need_for_check:
        if time.time() - timeout < 600:
            return Mailbox()
        
    # Reset the game
    user = None
    victim = None

    for player in winners:
        if player.user == acceptant:
            user = player
        if player.user == challenger:
            victim = player

    if victim == None:
        victim = Ruser(challenger)
        winners.append(victim)
    if user == None:
        user = Ruser(acceptant)
        winners.append(user)
    user.kill(victim)
    
    user.score += 1
    victim.score += -2
    update_roulette_score(user.user.id,user.score)
    update_roulette_score(victim.user.id,victim.score)

    answer = Mailbox().respond("It seems like <@{}> has chickened out! Boo!".format(victim.id),False,['🍅'])
    answer.respond("**<@{}> WINS!**".format(user.id))

    challenger = None
    acceptant = None
    game_channel = None

    bullet_number = 0
    bullet = 0
    timeout = 0

    return answer

def profile(user):
    global winners
    global deadies

    answer = '**__Profile of <@{}>:__**\n'.format(user.id)
    user_class = None

    for good_guy in winners:
        if user == good_guy.user:
            user_class = good_guy
    for bad_boy in deadies:
        if user == bad_boy.user:
            user_class = bad_boy
    
    if user_class == None:
        answer += "**Score: 0 points.\n*Play a game to get some points!*"
    else:
        answer += "**Score: {} point".format(user_class.score)
        if user_class.score != 1:
            answer += "s"
        answer += ".\n" + str(user_class)
    
    return Mailbox().respond(answer,True)