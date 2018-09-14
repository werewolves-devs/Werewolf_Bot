from flask import Blueprint, jsonify
from communication import webhook
import management.items as items
import management.boxes as box
import config
import json

bp = Blueprint(__name__, __name__)

def get_property_by_id(json_list, id):
    for element in json_list:
        if id == element["id"]:
            return element
    return None

@bp.route('/<token>/get_rewards')
def get_rewards(token):
    validity = box.token_status(token)
    if validity != 0:
        return jsonify(option1={"code": -1, "description": "NOT FOUND", "name": "NOT FOUND"},
            option2={"code": -1, "description": "NOT FOUND", "name": "NOT FOUND"},
            option3={"code": -1, "description": "NOT FOUND", "name": "NOT FOUND"},)

    given_options = items.get_rewards()
    box.add_source1(token,request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    box.add_options(token,given_options[0]["code"],given_options[1]["code"],given_options[2]["code"])

    # Make an announcement if any legendaries found
    legendary_amount = 0
    for option in given_options:
        if option["code"] > 4000000-1:
            legendary_amount += 1
    if legendary_amount > 3:
        print("Invalid amount of legendaries found.")
    if legendary_amount == 3:
        webhook.send_public_message("**NO WAY!** <@{}> just found ***THREE LEGENDARIES*** in a lootbox!\nThat's a chance of 1 in 1 MILLION!".format(box.get_token_data(token)[1]))
    if legendary_amount == 2:
        webhook.send_public_message("<@{}> just opened a lootbox with two legendaries! Wow!".format(box.get_token_data(token)[1]))
    if legendary_amount == 1:
        webhook.send_public_message("<@{}> just found a legendary item in a lootbox!".format(box.get_token_data(token)[1]))

    return jsonify(option1=given_options[0],option2=given_options[1],option3=given_options[2])


# Archive

@bp.route('/archive/list_seasons')
def list_seasons():
    return(jsonify({'status': '500', 'reason': 'Work-In-Progress'}))

@bp.route('/archive/get_messages/<season>/<int:channel_id>/<int:chunk>')
def get_messages(season, channel_id, chunk=0):
    with open("./archives/season_{}.json".format(season), encoding="utf8") as f:
        data = json.loads(f.read())
        guild = get_property_by_id(data["Guilds"], config.main_guild)
        channel = get_property_by_id(guild["Channels"], channel_id)
        messages = channel["Messages"]
        chunk = -50 * chunk
        chunk_of_messages = messages[chunk:]
        return jsonify(chunk_of_messages)

# General

@bp.route('/version/')
def show_version():
    return jsonify({
        'version': '1.0',
        'deprecated': False,
    })
