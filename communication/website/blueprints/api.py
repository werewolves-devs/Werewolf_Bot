from flask import Blueprint, jsonify, g, session, request, redirect
from requests_oauthlib import OAuth2Session
import os
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
    try:
        with open("./archives/season_{}.json".format(season), encoding="utf8") as f:
            data = json.loads(f.read())
            guild = get_property_by_id(data["Guilds"], config.main_guild)
            channel = get_property_by_id(guild["Channels"], channel_id)
            if channel == None:
                return jsonify({"status": 404, "reason": "Unknown Channel ID"})
            messages = channel["Messages"]
            chunk = -50 * chunk
            chunk_of_messages = messages[chunk:]
            return jsonify(chunk_of_messages)
    except:
        return jsonify({"status": 404, "reason": "Unknown Season"})

@bp.route('/archive/get_channels/<season>/')
def get_channels(season):
    try:
        with open("./archives/season_{}.json".format(season), encoding="utf8") as f:
            data = json.loads(f.read())
            guild = get_property_by_id(data["Guilds"], config.main_guild)
            if guild == None:
                return jsonify({"status": 404, "reason": "Unknown Guild ID"})
            channels = []
            for channel in guild["Channels"]:
                del channel["Messages"]
                channels.append(channel)
            return jsonify(channels)
    except:
        return jsonify({"status": 404, "reason": "Unknown Season"})

# Auth

api_base = 'https://discordapp.com/api'
TOKEN_URL = api_base + '/oauth2/token'

def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=config.oauth_id,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=config.oauth_callback,
        auto_refresh_kwargs={
            'client_id': config.oauth_id,
            'client_secret': config.oauth_secret,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

if 'http://' in config.oauth_callback:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

@bp.route('/auth/login')
def redirect_to_auth():
    scope = request.args.get(
        'scope',
        'identify'
    )
    discord = make_session(scope=scope.split(' '))
    auth_url, state = discord.authorization_url(api_base + '/oauth2/authorize')
    session['oauth2_state'] = state
    return redirect(auth_url)

@bp.route('/auth/callback')
def calllback():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=config.oauth_secret,
        authorization_response=request.url
    )
    session['oauth2_token'] = token
    return redirect('/')

@bp.route('/user/data')
def me():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(api_base + '/users/@me').json()
    return jsonify(user)

@bp.route('/user/is_logged_in')
def is_logged_in():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(api_base + '/users/@me').json()
    try:
        if user["code"] == 0:
            json = jsonify({'is_logged_in': False})
    except KeyError:
        json = jsonify({'is_logged_in': True})

    return json

# General

@bp.route('/version/')
def show_version():
    return jsonify({
        'version': '1.0',
        'deprecated': False,
    })
