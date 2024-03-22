import logging
import sqlite3

from src.modules import UserInDB


class UsersDB():
    def __init__(self) -> None:
        self.db = sqlite3.connect('users.bd')
        self.sql = self.db.cursor()

        self.sql.execute("""CREATE TABLE IF NOT EXISTS users (
                    name TEXT,
                    hashedPassword TEXT,
                    email TEXT,
                    disabled BOOLEAN
        )""")
        self.db.commit()

    def create_user(this, user_name, user_password, user_emeil):
        logger = logging.getLogger("uvicorn.error")
        logger.info("created")
        if (user_name == None) or (user_password == None):
            return False
        
        this.sql.execute(f"SELECT name FROM users WHERE name = '{user_name}'")
        if this.sql.fetchone() is None:
            this.sql.execute("INSERT INTO users VALUES (?,?,?,?)", (user_name, user_password, user_emeil, False))
            this.db.commit()
            # добавлен новый пользователь
        else:
            return Exception("user with this name already exists")

    def get_user(this, user_name):
        if (user_name == None):
            return None

        this.sql.execute("SELECT * FROM users WHERE name = ?", (user_name,) )
        db_user = this.sql.fetchone()
        user = UserInDB(username=db_user[0], email=db_user[2], disabled=db_user[3], hashed_password=db_user[1])
        return user


    def getAllUsers(this):
        list_users = list()
        for value in this.sql.execute("SELECT * FROM users"):
            list_users.append(value)

        return list_users
    
    def delete(this):
        this.sql.execute("DROP TABLE IF EXISTS users")


# all_users = UsersDB()

# print(all_users.create_user('Amir', 'ggggggs', 'amralt@gmail.com'))
# print(all_users.get_user("Amir"))

# print(all_users.getAllUsers())
# print(all_users.get_user_password('amir'))