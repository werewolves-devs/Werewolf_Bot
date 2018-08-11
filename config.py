from configparser import ConfigParser

config = ConfigParser()

with open('config.ini') as fp:
    config.read_file(fp)

discord = config['discord']

TOKEN = discord['token']

# Rules 'n' settings
max_channels_per_category = int(discord['max_channels_per_category'])
max_participants = int(discord['max_participants'])
max_cc_per_user = int(discord['max_cc_per_user'])
season = discord['season']

ww_prefix = discord['ww_prefix']
act_prefix = discord['act_prefix']

# List of specific roles
roles = config['roles']

administrator = int(roles['administrator'])
game_master = int(roles['game_master'])
participant = int(roles['participant'])
dead_participant = int(roles['dead_participant'])
frozen_participant = int(roles['frozen_participant'])
# TODO
suspended = int(roles['suspended'])

# List of specific channels
channels = config['channels']
welcome_channel = int(channels['welcome_channel'])
game_log = int(channels['game_log'])
bot_spam = int(channels['bot_spam'])
story_time = int(channels['story_time'])

# Database settings
database = config['database']
dynamic_config = database['dynamic_config']
general_database = database['general_database']
database = database['database']
