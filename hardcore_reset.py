import reset
import config
import sqlite3
import os
from shutil import copy
from management.items import jget

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

    # Despite confirmations, make one last back-up
    newpath = 'backup/last_reset'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    open('backup/last_reset/backup_game.db', 'a').close()
    open('backup/last_reset/backup_general.db', 'a').close()
    open('backup/last_reset/backup_stats.json', 'a').close()
    open('backup/last_reset/backup_dynamic.json', 'a').close()
    open('backup/last_reset/backup_config.py', 'a').close()
    copy(config.database,'backup/last_reset/backup_game.db')
    copy(config.general_database,'backup/last_reset/backup_general.db')
    copy(config.stats_file,'backup/last_reset/backup_stats.json')
    copy(config.dynamic_config,'backup/last_reset/backup_dynamic.json')
    copy('config.py','backup/last_reset/backup_config.py')

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
    c.execute("DROP TABLE IF EXISTS 'sources'")
    if skip == False:
        print('Progress deleted!\n')
        print('Creating space for a new database....')
    inventory_table = "CREATE TABLE 'inventory' ('id' INTEGER NOT NULL, 'name' TEXT NOT NULL, "
    for item in jget("items"):
        inventory_table += "'{}' INTEGER NOT NULL DEFAULT 0, ".format(item["code"])
    inventory_table +="PRIMARY KEY('id'));"
    c.execute(inventory_table)
    
    c.execute("CREATE TABLE 'users' ('id' INTEGER NOT NULL, 'name' TEXT NOT NULL, 'credits' INTEGER NOT NULL DEFAULT 0, 'activity' INTEGER NOT NULL DEFAULT 0, 'roulette_record' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('id'));")
    c.execute("CREATE TABLE 'activity' ('id' INTEGER NOT NULL, 'name' TEXT NOT NULL, 'activity' INTEGER NOT NULL DEFAULT 0, 'spam_activity' REAL NOT NULL DEFAULT 0, 'spam_filter' INTEGER NOT NULL DEFAULT 200, 'record_activity' REAL NOT NULL DEFAULT 0, FOREIGN KEY(`id`) REFERENCES `users`(`id`), PRIMARY KEY('id'));")
    c.execute("CREATE TABLE 'offers' ('id' INTEGER NOT NULL, 'emoji' TEXT NOT NULL, 'price' INTEGER NOT NULL, 'owner' INTEGER NOT NULL, FOREIGN KEY(`id`) REFERENCES `users`(`id`));")
    c.execute("CREATE TABLE 'requests' ('id' INTEGER NOT NULL, 'emoji' TEXT NOT NULL, 'price' INTEGER NOT NULL, 'owner' INTEGER NOT NULL, FOREIGN KEY(`id`) REFERENCES `users`(`id`));")
    c.execute("CREATE TABLE 'tokens' ( `token` TEXT NOT NULL, `owner` INTEGER NOT NULL, `status` INTEGER NOT NULL DEFAULT 0, `opt1` NUMERIC, `opt2` TEXT, `opt3` TEXT, `choice` TEXT, `source1` TEXT, `source2` TEXT, `creation` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, `redeemed` TEXT, `message` INTEGER NOT NULL, FOREIGN KEY(`owner`) REFERENCES `users`(`id`), PRIMARY KEY(`token`,`message`) )")
    c.execute("CREATE TABLE 'shops' ('message' INTEGER NOT NULL, 'age' INTEGER NOT NULL DEFAULT 0, PRIMARY KEY('message'));")
    c.execute("CREATE TABLE 'sources' ('user' INTEGER NOT NULL, 'source' TEXT NOT NULL, 'amount' INTEGER NOT NULL DEFAULT 1, FOREIGN KEY(`user`) REFERENCES `users`(`id`));")
    print('Formatting completed! The bot is now ready for a new game!\n')

    if skip == False:
        input("Press any button to exit this program.")

if __name__ == "__main__":
    hard_reset()