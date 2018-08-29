import reset
import config
import sqlite3

conn = sqlite3.connect(config.general_database)
c = conn.cursor()

def hard_reset(skip = False):
    if skip == False:
        confirm = input("Are you sure you want to reset the data? Any current game progress will be deleted.\nType 'Yes' to proceed. ")
        if confirm != 'Yes':
            print('Resetting canceled.')
            return
        confirm = input("Are you VERY sure? Not only will this delete the game database, also will it lose any other records.\nType 'Yes' to proceed. ")
        if confirm != 'Yes':
            print('Resetting canceled.')
            return

    # Reset the game table.
    reset.reset(True)
    print('\nDeleting any remaining data...')
    c.execute("DROP TABLE IF EXISTS 'offers'")
    c.execute("DROP TABLE IF EXISTS 'requests'")
    c.execute("DROP TABLE IF EXISTS 'tokens'")
    c.execute("DROP TABLE IF EXISTS 'prizes'")
    c.execute("DROP TABLE IF EXISTS 'shops'")
    if skip == False:
        print('Progress deleted!\n')
        print('Creating space for a new database....')
    c.execute("CREATE TABLE 'offers' ('id' INTEGER NOT NULL, 'emoji' TEXT NOT NULL, 'price' INTEGER NOT NULL, 'owner' INTEGER NOT NULL, PRIMARY KEY('id'));")
    c.execute("CREATE TABLE 'requests' ('id' INTEGER NOT NULL, 'emoji' TEXT NOT NULL, 'price' INTEGER NOT NULL, 'owner' INTEGER NOT NULL, PRIMARY KEY('id'));")
    c.execute("CREATE TABLE 'tokens' ('token' TEXT NOT NULL, 'owner' INTEGER NOT NULL, 'status' INTEGER NOT NULL DEFAULT 0, 'opt1' TEXT, 'opt2' TEXT, 'opt3' TEXT, 'choice' TEXT, 'source1' TEXT, 'source2' TEXT, PRIMARY KEY('token'));")
    c.execute("CREATE TABLE 'prizes' ('prize' INTEGER NOT NULL, 'option' INTEGER NOT NULL DEFAULT 0, 'choice' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('prize'));")
    c.execute("CREATE TABLE 'shops' ('message' INTEGER NOT NULL, 'age' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('message'));")
    print('Formatting completed! The bot is now ready for a new game!\n')

    if skip == False:
        input("Press any button to exit this program.")

if __name__ == "__main__":
    hard_reset()
