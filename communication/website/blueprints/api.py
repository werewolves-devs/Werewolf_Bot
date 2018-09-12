from flask import Blueprint, jsonify

bp = Blueprint(__name__, __name__)

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

@bp.route('/version/')
def show_version():
    return jsonify({
        'version': '1.0',
        'deprecated': False,
    })
