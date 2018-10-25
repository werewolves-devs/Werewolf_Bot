from enum import Enum

import roles_n_rules.wrappers as wrap
from main_classes import Mailbox

def role_functions(role_name):
    """Gain a role's class by name. Spaces are replaced by underscores.  
    :role_name: The name of the role."""
    return globals()[role_name]()

def get_powers(role_name):
    """Test if a certain command is a valid role-related command. Injection proof."""
    return [item[6:] for item in globals()[role_name].__dict__ if item.startswith('power_')]

def std_day(self):
    self.sleepingover = False
    self.fakerole = self.role
    self.protected = False

def std_night(self):
    self.votes = 1
    self.threatened = False
    self.bitten = False

next = '|            '
success = '|---> '
failure = '|'
skull = '💀 '

# ------------------------------------

class Team(Enum):
    # General role teams
    village = 0
    wolf = 1
    solo = 2

    # Specific role teams

# ------------------------------------

class Innocent:
    team = Team.village
    
    def start(self):
        pass

    def day(self,number):
        std_day(self)

    def night(self,number):
        std_night(self)

    @wrap.protected
    @wrap.abducted
    @wrap.frozen
    @wrap.souls
    def attack(self,murderer,answer=Mailbox(),recursive='\n'):
        # TODO: Get the victim's standoff list, and check if it has an executioner standoff.
        replacements = [standoff for standoff in db.get_standoff(user_id) if standoff[2] == 'Executioner']

        if replacements == []:
            answer.log_add(recursive + success + skull + '<@{}> was killed by an angry mob.'.format(user_id))
            answer = instant_death(user_id, role, answer, recursive+next)
            
        else:
            answer.log_add(recursive + success + '<@{}> escaped death as the Executioner.')
            
            if user_role == 'Executioner':
                db_set(user_id,'role','Innocent')

            for standoff in replacements:
                db.delete_standoff(standoff[0])
                answer = instant_death(standoff[1], standoff[2], answer, recursive+next)

        return answer
    
    def has_won_game(self,user_list):
        for other in user_list:
            if other.alive and other.team != Team.village:
                return False
        return True

class Assassin(Innocent):
    team = Team.village
    
    def start(self):
        #TODO: Create a secret channel.
        pass
    
    def day(self,number):
        std_day(self)
        self.uses = 0
    
    def night(self,number):
        std_night(self)

        if number > 1:
            self.uses = 1
    
    @wrap.abducted
    @wrap.frozen
    @wrap.sleepingover
    @wrap.protected
    @wrap.souls
    @wrap.demonized
    def attack(self,murderer,answer=Mailbox(),recursive='\n'):
        answer.log_add(recursive + success + skull + '<@{}> was assassinated.'.format(user_id))
        answer = instant_death(self, "Assassin", answer, recursive+next)
        return answer

class Aura_Teller(Assassin):
    team = Team.village
    
    def night(self,number):
        std_night(self)
        self.uses = 1

class Baker(Innocent):
    team = Team.village
    
    def start(self):
        # TODO: Create a secret channel with all other bakers.
        pass
    
class Butcher(Innocent):
    team = Team.village
    
    def start(self):
        # TODO: Create a secret channel with all other butchers and bloody butchers.
        pass

class Barber(Innocent):
    team = Team.village
    
    def start(self):
        # TODO: Create a secret channel.
        pass
    
    def day(self,number):
        std_day(self)
        self.uses = 1
    
    def night(self,number):
        std_night(self)
        self.uses = 0
    
    @wrap.abducted
    @wrap.frozen
    @wrap.protected
    @wrap.souls
    def attack(self,murderer,answer=Mailbox(),recursive='\n'):
        answer.log_add(recursive + success + skull + '<@{}> was cut into little pieces.'.format(user_id))
        answer = instant_death(self, "Barber", answer, recursive+next)
        return answer

class Crowd_Seeker(Assassin):
    team = Team.village
    
    def night(self,number):
        std_night(self)
        self.uses = 3

class Cult_Leader(Innocent):
    team = Team.village
    
    def start(self):
        # TODO: Create a secret channel with all other cult members and cult leaders.
        pass

    @wrap.abducted
    @wrap.frozen
    @wrap.protected
    @wrap.sleepingover
    @wrap.souls
    @wrap.demonized
    def attack(self,murderer,answer=Mailbox(),recursive='\n'):
        answer.log_add(recursive + success + skull + '<@{}> was killed by the cult.'.format(user_id))
        answer = instant_death(self, "Cult Leader", answer, recursive+next)
        return answer

class Cult_Member(Cult_Leader):
    team = Team.village

class Cupid:
    team = Team.village
    
    # TODO
    pass

class Cursed_Civilian(Innocent):
    team = Team.village

class Dog(Innocent):
    team = Team.village
    
    def start(self):
        pass # TODO: Create na secret channel
    
    def day(self,number):
        std_day(self)
        if number > 0:
            pass # TODO: Turn the player into an Innocent.
    
    def night(self,number):
        std_night(self)
        self.uses = 1

class Executioner(Innocent):
    team = Team.village
    
    def start(self):
        print("It worked!")

    def power_execute(self):
        pass # TODO: Add threat to player

class Exorcist(Innocent):
    team = Team.village
    
    def start(self):
        pass # TODO: create a secret channel.
    
class Fortune_Teller(Innocent):
    team = Team.village
    
    def start(self):
        pass # TODO: create a secret channel.
    
    def day(self):
        std_day(self)
        self.uses = 0
    
    def night(self):
        std_night(self)
        self.uses = 1

    def attack(self,murderer,answer=Mailbox(),recursive='\n'):
        if self.undead:
            answer.dm("Your idol, the fortune teller <@{}>, has deceased. ".format(murderer),self.id)
            answer.dm_add("They were a great inspiration to you... ")
            answer.dm_add("back when you were alive, at least. Now, your undead heart is as cold as it has ever been, ")
            answer.dm_add("and nothing will happen to you.\n")
            answer.dm_add("**The rules do not change. You will remain Undead.**")
            answer.log_add(recursive + success + '<@{}> failed to become a Fortune Teller.'.format(self.id))
            return answer            

        answer.dm("Your idol, the fortune teller <@{}>, has deceased. ".format(murderer),self.id)
        answer.dm_add("They were a great inspiration to you, and that's why ")
        answer.dm_add("you've decided to get in their footsteps!\n")
        answer.dm_add("**You have turned into a Fortune Teller. Find and ")
        answer.dm_add("eliminate all werewolves, solo players and other enemies!**")
        answer.log_add(recursive + success + '<@{}> became a Fortune Teller.'.format(self.id))
        return answer
    
    @wrap.require_uses
    @wrap.require_users(1)
    @wrap.power_abducted
    def power_inspect(self,numbers,roles,users):
        other = users[0]
        self.uses += -1

        if other.role == other.fakerole and other.undead:
            return Mailbox().respond("{} - <@{}> has the role of the `Undead`!".format(other.emoji,other.id))
        return Mailbox().respond("{} - <@{}> has the role of the `{}`!".format(other.emoji,other.id,other.fakerole))


class Fortune_Apprentice(Innocent):
    team = Team.village
    
    def start(self):
        pass # TODO: Create a secret channel.

class Grandma(Innocent):
    team = Team.village

    def start(self):
        pass # TODO: Create a secret channel.
    
    def day(self,number):
        std_day(self)
        self.uses = 0
    
    def night(self,number):
        std_night(self)
        self.uses = 3
    
    @wrap.require_uses
    @wrap.require_users(1)
    def power_grandma(self,numbers,roles,users):
        pass # TODO