import management.db as db
import reset

def database_check():
    role = db.db_test()
    reset.reset(True)
    return role

if __name__ == "__main__":
    print(database_check())
