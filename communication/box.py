import management.boxes as box
import config
from requests import get

def request_token(user_id):
    """Request a lootbox token from the API.
    The function returns a string, which is the URL to the lootbox in a string format.

    Keyword arguments:
    user_id -> user for whom the lootbox is meant."""

    url = config.base_url + "/api/create_lootbox.php?auth_token=" + config.box_token + "&discord_id=" + user_id

    response = get(url).text
    if '200' not in response:
        # There's an Error
        print("Nah fam ya gotta check your error: " + response)
        return

    return response.split(":")[1]

def delete_token(token):
    """Request the API to invalidate a given token.
    This function can be used for timeouts, invalid requests, specific retractions or cleaning up the database.

    Keyword arguments:
    token -> the token that needs to be made invalid."""

    # To be filled in by BenTechy66
    return '4GdrR4^Y7uyyR'
