import matplotlib.pyplot as plt
import sqlite3
import os

def user_activity(user):
    numbertable = []
    directory = []
    for folder1 in os.listdir():
        if folder1 not in ['last_reset','stats.py','users']:
            year = int(folder1.split('_')[0])
            month = int(folder1.split('_')[1])
            directory.append(year*100+month)

    directory.sort()
    for code in directory:
        folder1 = '{}_{}'.format(code//100,code%100)
        for folder2 in os.listdir(folder1):
            for backup in os.listdir(folder1 + '/' + folder2):
                if 'backup_general' in backup:

                    conn = sqlite3.connect(folder1 + '/' + folder2 + '/' + backup)
                    c = conn.cursor()

                    try:
                        c.execute('SELECT activity FROM \'users\' WHERE id=?',(user,))
                    except Exception:
                        print("Table not found in file {}.".format(folder1 + '/' + folder2 + '/' + backup))
                    else:
                        answer = c.fetchone()

                        if answer == None:
                            numbertable.append(0)
                        else:
                            numbertable.append(answer[0])
                    
                    conn.close()
    
    return numbertable

users = [248158876799729664,140424290171486208,125449182663278592,246334877287317504,482863919111733248]

for user in users:
    numbertable = user_activity(user)
    plt.plot(range(len(numbertable)),numbertable)

if len(users) == 1:
    plt.savefig('users/' + str(user))

plt.savefig('users/temp')
plt.show()