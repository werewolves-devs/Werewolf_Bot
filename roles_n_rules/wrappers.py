from functools import wraps

next = '|            '
success = '|---> '
failure = '|'
skull = '💀 '

def demonized(func):
    @wraps(func)
    def validate_if_demonized(*args,**kwargs):
        if args[0].demonized == True:
            # TODO: Make the user undead.
            pass
        return func(*args,**kwargs)
    return validate_if_demonized

def sleepingover(func):
    @wraps(func)
    def validate_if_sleepingover(*args,**kwargs):
        if args[0].sleepingover == True:
            # TODO: Cancel the attack.
            pass
        return func(*args,**kwargs)
    return validate_if_sleepingover

def frozen(func):
    @wraps(func)
    def validate_if_frozen(*args,**kwargs):
        if args[0].frozen == True:
            # TODO: Cancel the attack.
            pass
        return func(*args,**kwargs)
    return validate_if_frozen

def souls(func):
    @wraps(func)
    def validate_if_souls(*args,**kwargs):
        if args[0].souls > 0:
            # TODO: Make the user undead.
            pass
        return func(*args,**kwargs)
    return validate_if_souls

def protected(func):
    @wraps(func)
    def validate_if_protected(*args,**kwargs):
        if args[0].protected == True:
            # TODO: Cancel the attack.
            pass
        return func(*args,**kwargs)
    return validate_if_protected

def abducted(func):
    @wraps(func)
    def validate_if_abducted(*args,**kwargs):
        if args[0].abducted == True:
            # TODO: Cancel the attack.
            pass
        return func(*args,**kwargs)
    return validate_if_abducted

def require_uses(func):
    @wraps(func)
    def more_than_zero_uses(*args,**kwargs):
        if args[0].uses > 0:
            return func(*args,**kwargs)
        pass # TODO: Cancel the power
    return more_than_zero_uses

def require_numbers(amount):
    def search_numbers(func):
        @wraps(func)
        def look_for_numbers(self,numbers,roles,users):
            if len(numbers) < amount:
                pass # TODO: Cancel powers due to no integers provided.
            return func(self,numbers,roles,users)
        return look_for_numbers
    return search_numbers

def require_roles(amount):
    def search_roles(func):
        @wraps(func)
        def look_for_roles(self,numbers,roles,users):
            if len(roles) < amount:
                pass # TODO: Cancel powers due to no integers provided.
            return func(self,numbers,roles,users)
        return look_for_roles
    return search_roles

def require_users(amount):
    def search_users(func):
        @wraps(func)
        def look_for_users(self,numbers,roles,users):
            for user in users:
                if not user.participant:
                    users.remove(user)
            if len(users) < amount:
                pass # TODO: Cancel powers due to no roles provided
            return func(self,numbers,roles,users)
        return look_for_users
    return search_users

def power_abducted(func):
    @wraps(func)
    def remove_abducted_players(self,numbers,roles,users):
        for other in users:
            if other.abducted:
                pass # TODO: Cancel power due to targeting an abducted player.
        
        return func(self,numbers,roles,users)
    return remove_abducted_players