import config
import stats
import sqlite3

conn = sqlite3.connect(config.database)
c = conn.cursor()

def reset(skip = False):
    if skip == False:
        confirm = input("Are you sure you want to reset the data? Any current game progress will be deleted.\nType 'Yes' to proceed. ")
        if confirm != 'Yes':
            print('Resetting canceled.')
            return

    print("\nWiping stats...")
    if stats.reset_stats(True):
        print("\nSuccessfully reset stats")
    else:
        print("\n-----\nWARNING: Stats wipe failed\n-----\n")

    # Reset the game table.
    print('\nDeleting any old progress...')
    c.execute("DROP TABLE IF EXISTS 'game'")
    c.execute("DROP TABLE IF EXISTS 'death-row'")
    c.execute("DROP TABLE IF EXISTS 'polls'")
    c.execute("DROP TABLE IF EXISTS 'channels'")
    c.execute("DROP TABLE IF EXISTS 'channel_rows'")
    c.execute("DROP TABLE IF EXISTS 'categories'")
    c.execute("DROP TABLE IF EXISTS 'secret_categories'")
    c.execute("DROP TABLE IF EXISTS 'freezers'")
    c.execute("DROP TABLE IF EXISTS 'standoff'")
    c.execute("DROP TABLE IF EXISTS 'role-pool'")
    c.execute("DROP TABLE IF EXISTS 'secret_channels'")
    c.execute("DROP TABLE IF EXISTS 'deadies'")
    c.execute("DROP TABLE IF EXISTS 'listener'")
    c.execute("DROP TABLE IF EXISTS 'trashcan'")
    c.execute("DROP TABLE IF EXISTS 'trashy'")
    if skip == False:
        print('Progress deleted!\n')
        print('Creating space for a new game....')
    c.execute("CREATE TABLE 'game' ('id' INTEGER NOT NULL, 'name' TEXT NOT NULL, 'emoji' TEXT NOT NULL, 'activity' INTEGER NOT NULL DEFAULT 0, 'channel' INTEGER NOT NULL DEFAULT {}, 'role' TEXT NOT NULL DEFAULT 'Spectator', 'fakerole' TEXT NOT NULL DEFAULT 'Spectator', 'uses' INTEGER NOT NULL DEFAULT 0, 'votes' INTEGER NOT NULL DEFAULT 1, 'threatened' INTEGER NOT NULL DEFAULT 0, 'enchanted' INTEGER NOT NULL DEFAULT 0, 'demonized' INTEGER NOT NULL DEFAULT 0, 'powdered' INTEGER NOT NULL DEFAULT 0, 'frozen' INTEGER NOT NULL DEFAULT 0, 'undead' INTEGER NOT NULL DEFAULT 0, 'bites' INTEGER NOT NULL DEFAULT 0, 'bitten' INTEGER NOT NULL DEFAULT 0, 'souls'	INTEGER NOT NULL DEFAULT -1, 'sleepingover' INTEGER NOT NULL DEFAULT 0, 'lastwords' TEXT NOT NULL DEFAULT '', 'abducted' INTEGER NOT NULL DEFAULT 0, 'ccs' INTEGER NOT NULL DEFAULT 0, 'horseman' INTEGER NOT NULL DEFAULT 0, 'amulet' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('id','emoji'));".format(config.game_log))
    c.execute("CREATE TABLE 'death-row' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'victim' TEXT NOT NULL, 'role' TEXT NOT NULL, 'murderer' TEXT NOT NULL DEFAULT '')")
    c.execute("CREATE TABLE 'categories' ('current' INTEGER NOT NULL DEFAULT 1, 'id' TEXT NOT NULL, 'channels' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('id'));")
    c.execute("CREATE TABLE 'secret_categories' ('current' INTEGER NOT NULL DEFAULT 1, 'id' TEXT NOT NULL, 'channels' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('id'));")
    c.execute("CREATE TABLE 'channels' ('channel_id' TEXT PRIMARY KEY NOT NULL, 'owner' TEXT NOT NULL)")
    c.execute("CREATE TABLE 'channel_rows' ('id' INTEGER PRIMARY KEY NOT NULL)")
    c.execute("CREATE TABLE 'freezers' ('king' INTEGER NOT NULL, 'victim' INTEGER NOT NULL, 'role' TEXT NOT NULL)")
    c.execute("CREATE TABLE 'standoff' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'victim' TEXT NOT NULL, 'role' TEXT NOT NULL, 'murderer' TEXT NOT NULL);")
    c.execute("CREATE TABLE 'role-pool' ('role' TEXT PRIMARY KEY NOT NULL, 'amount' INTEGER NOT NULL DEFAULT 0 )")
    c.execute("CREATE TABLE 'secret_channels' ('role' TEXT NOT NULL, `channel_id` INTEGER NOT NULL, PRIMARY KEY('channel_id'));")
    c.execute("CREATE TABLE 'deadies' ('user_id' INTEGER NOT NULL PRIMARY KEY);")
    c.execute("CREATE TABLE 'listener' ('innocent' INTEGER NOT NULL, 'spy' INTEGER NOT NULL);")
    c.execute("CREATE TABLE 'trashcan' ('message' INTEGER NOT NULL, 'channel' INTEGER NOT NULL, PRIMARY KEY('message'));")
    c.execute("CREATE TABLE 'trashy' ('channel' INTEGER NOT NULL, PRIMARY KEY('channel'));")
    number = float(config.max_participants)/20
    if number > int(number):
        number += 1
    number = int(number)

    poll_str = "CREATE TABLE 'polls' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'purpose' TEXT NOT NULL, 'user_id' INTEGER NOT NULL, 'channel' INTEGER NOT NULL, 'part1' INTEGER NOT NULL DEFAULT 0"
    for i in range(number - 1):
        poll_str += ", 'part{}' INTEGER NOT NULL DEFAULT 0".format(i+2)
    poll_str += ")"
    c.execute(poll_str)
    print('Formatting completed! The bot is now ready for a new game!\n')

    if skip == False:
        input("Press any button to exit this program.")

if __name__ == "__main__":
    reset()
