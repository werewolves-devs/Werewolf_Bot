def role_functions(role_name) -> object:
    """Gain a role's class by name. Spaces are replaced by underscores.  
    :role_name: The name of the role."""
    return globals()[role_name]()

class Innocent:
    def start(self):
        pass

    def day(self):
        self.sleepingover = False
        self.fakerole = self.role

    def night(self):
        self.votes = 1

