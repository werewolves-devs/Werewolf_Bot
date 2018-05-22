import config
import sqlite3

conn = sqlite3.connect(config.database)
c = conn.cursor()

def reset():
    confirm = input("Are you sure you want to reset the data? Any current game progress will be deleted.\nType 'Yes' to proceed. ")
    if confirm != 'Yes':
        print('Resetting canceled.')
        return

    # Reset the game table.
    print('\nDeleting any old progress...')
    c.execute("DROP TABLE 'game'")
    c.execute("DROP TABLE 'kill_queue'")
    print('Progress deleted!\n')
    print('Creating space for a new game....')
    c.execute("CREATE TABLE 'game' ('id' TEXT NOT NULL, 'name' TEXT NOT NULL, 'emoji' TEXT NOT NULL, 'activity' INTEGER NOT NULL DEFAULT 0 , 'channel' TEXT NOT NULL DEFAULT '{}', 'role' TEXT NOT NULL DEFAULT 'Spectator', 'fakerole' TEXT NOT NULL DEFAULT 'Spectator', 'uses' INTEGER NOT NULL DEFAULT 0 , 'votes' INTEGER NOT NULL DEFAULT 1 , 'threatened' INTEGER NOT NULL DEFAULT 0 , 'enchanted' INTEGER NOT NULL DEFAULT 0 , 'demonized' INTEGER NOT NULL DEFAULT 0 , 'powdered' INTEGER NOT NULL DEFAULT 0 , 'frozen' INTEGER NOT NULL DEFAULT 0 , 'undead' INTEGER NOT NULL DEFAULT 0 , 'bites' INTEGER NOT NULL DEFAULT 0 , 'bitten' INTEGER NOT NULL DEFAULT 0 , 'souls' INTEGER NOT NULL DEFAULT -1 , 'lovers' TEXT, 'sleepers' TEXT, 'amulets' TEXT, 'zombies' TEXT, PRIMARY KEY ('id', 'name', 'emoji'))".format(config.game_log))
    c.execute("CREATE TABLE 'kill_queue' ('victim' TEXT NOT NULL, 'role' TEXT NOT NULL, 'murderer' TEXT)")
    print('Formatting completed! The bot is now ready for a new game!\n')

    input("Press any button to exit this program.")

if __name__ == "__main__":
    reset()
