from enum import Enum

# Discord API / Login settings
WW_TOKEN = "yo_mommas_token"
TM_TOKEN = "yo_poppas_token"
DV_TOKEN = "yo_devils_token"
GH_TOKEN = "yo_deadies_token"

WEBHOOK_PUBLIC_ID = "mah_fancy_id"
WEBHOOK_PUBLIC_TOKEN = "mah_fancy_token"
WEBHOOK_PRIVATE_ID = "yah_fancy_id"
WEBHOOK_PRIVATE_TOKEN = "yah_fancy_token"

# Rules 'n' settings
max_channels_per_category = 50
max_participants = 40
max_cc_per_user = 8
activity_hours = 72
season = "0"

ww_prefix = '!'
ghost_prefix = '$'
devil_prefix = '+'
universal_prefix = "#!003-88-6521"

# Database settings
dynamic_config = "storage/dynamic.json"
general_database = 'storage/general.db'
database = 'storage/game.db'
shop_file = 'storage/shop.json'
stats_file = 'storage/stats.json'
item_file = 'storage/items.json'
max_channels_per_category = 50

# List of specific channels
class Destination(Enum):
    welcome_channel = 425036088239980544
    game_log = 485843514379337748
    bot_spam = 394541968689987584
    story_time = 485843933625188352
    market_channel = 493725561269780500
    quotes = 487354468606803968

# List of specific roles
class Role(Enum):
    administrator = 400956179561447425
    game_master = 375651524950360075
    participant = 380494164627816448
    dead_participant = 380493972100874242
    frozen_participant = 432146998762668033
    suspended = 382947666935414784
    peasant = 396041262836351006

    mayor = 382103216105717760
    reporter = 382103338550034442
