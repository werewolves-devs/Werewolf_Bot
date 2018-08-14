from management import db, dynamic as dy, setup
from management.db import db_get, db_set

def pay():
    """This function takes care of all properties that need to happen in the first wave of the end of the night.
    The function returns a Mailbox."""

    answer = Mailbox(True)
    for user in db.player_list():
        user_role = db_get(user,'role')

        # Remove tanner disguises
        db_set(user,'fakerole',user_role)
