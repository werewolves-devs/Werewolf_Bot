import matplotlib.pyplot as plt
import sqlite3
import os

user = 248158876799729664

numbertable = []
for folder1 in os.listdir():
    if folder1 not in ['last_reset','stats.py','users']:
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

plt.plot(range(len(numbertable)),numbertable,'r-')
plt.savefig('users/' + str(user))

plt.show()