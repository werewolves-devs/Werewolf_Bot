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
    c.execute("DROP TABLE IF EXISTS 'inventory'")
    c.execute("DROP TABLE IF EXISTS 'users'")
    c.execute("DROP TABLE IF EXISTS 'activity'")
    c.execute("DROP TABLE IF EXISTS 'offers'")
    c.execute("DROP TABLE IF EXISTS 'requests'")
    c.execute("DROP TABLE IF EXISTS 'tokens'")
    c.execute("DROP TABLE IF EXISTS 'prizes'")
    c.execute("DROP TABLE IF EXISTS 'shops'")
    if skip == False:
        print('Progress deleted!\n')
        print('Creating space for a new database....')
    c.execute("CREATE TABLE 'inventory' ('id' INTEGER NOT NULL, 'name' TEXT NOT NULL, \
	'000' INTEGER NOT NULL DEFAULT 0, \
	'001' INTEGER NOT NULL DEFAULT 0, \
	'002' INTEGER NOT NULL DEFAULT 0, \
	'003' INTEGER NOT NULL DEFAULT 0, \
	'004' INTEGER NOT NULL DEFAULT 0, \
	'005' INTEGER NOT NULL DEFAULT 0, \
	'006' INTEGER NOT NULL DEFAULT 0, \
	'007' INTEGER NOT NULL DEFAULT 0, \
	'008' INTEGER NOT NULL DEFAULT 0, \
	'009' INTEGER NOT NULL DEFAULT 0, \
	'010' INTEGER NOT NULL DEFAULT 0, \
	'011' INTEGER NOT NULL DEFAULT 0, \
	'012' INTEGER NOT NULL DEFAULT 0, \
	'013' INTEGER NOT NULL DEFAULT 0, \
	'014' INTEGER NOT NULL DEFAULT 0, \
	'015' INTEGER NOT NULL DEFAULT 0, \
	'100' INTEGER NOT NULL DEFAULT 0, \
	'101' INTEGER NOT NULL DEFAULT 0, \
	'102' INTEGER NOT NULL DEFAULT 0, \
	'103' INTEGER NOT NULL DEFAULT 0, \
	'104' INTEGER NOT NULL DEFAULT 0, \
	'105' INTEGER NOT NULL DEFAULT 0, \
	'106' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('id'));")
    c.execute("CREATE TABLE 'users' ('id' INTEGER NOT NULL, 'name' TEXT NOT NULL, 'credits' INTEGER NOT NULL DEFAULT 0, 'activity' INTEGER NOT NULL DEFAULT 0, 'age' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('id'));")
    c.execute("CREATE TABLE 'activity' ('id' INTEGER NOT NULL, 'name' TEXT NOT NULL, 'activity' INTEGER NOT NULL DEFAULT 0, 'spam_activity' REAL NOT NULL DEFAULT 0, 'spam_filter' INTEGER NOT NULL DEFAULT 200, 'record_activity' REAL NOT NULL DEFAULT 0, PRIMARY KEY('id'));")
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
