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

class Innocent:
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
    def attack(self,murderer,answer=Mailbox().log(''),recursive='\n'):
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

class Assassin(Innocent):
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
    def attack(self,murderer,answer=Mailbox().log(''),recursive='\n'):
        answer.log_add(recursive + success + skull + '<@{}> was assassinated.'.format(user_id))
        answer = instant_death(self, "Assassin", answer, recursive+next)
        return answer

class Aura_Teller(Assassin):
    def night(self,number):
        std_night(self)
        self.uses = 1

class Baker(Innocent):
    def start(self):
        # TODO: Create a secret channel with all other bakers.
        pass
    
class Butcher(Baker):
    def start(self):
        # TODO: Create a secret channel with all other butchers and bloody butchers.
        pass

class Barber(Innocent):
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
    def attack(self,murderer,answer=Mailbox().log(''),recursive='\n'):
        answer.log_add(recursive + success + skull + '<@{}> was cut into little pieces.'.format(user_id))
        answer = instant_death(self, "Barber", answer, recursive+next)
        return answer

class Crowd_Seeker(Assassin):
    def night(self,number):
        std_night(self)
        self.uses = 3

class Cult_Leader(Innocent):
    def start(self):
        # TODO: Create a secret channel with all other cult members and cult leaders.
        pass

    @wrap.abducted
    @wrap.frozen
    @wrap.protected
    @wrap.sleepingover
    @wrap.souls
    @wrap.demonized
    def attack(self,murderer,answer=Mailbox().log(''),recursive='\n'):
        answer.log_add(recursive + success + skull + '<@{}> was killed by the cult.'.format(user_id))
        answer = instant_death(self, "Cult Leader", answer, recursive+next)
        return answer

class Cult_Member(Cult_Leader):
    pass

