import sqlite3

from src.modules import UserInDB


class UsersDB():
    def __init__(self) -> None:
        self.db = sqlite3.connect('users.bd')
        self.sql = self.db.cursor()

        self.sql.execute("""CREATE TABLE IF NOT EXISTS users (
                    name TEXT,
                    hashedPassword TEXT
        )""")
        self.db.commit()

    def create_user(this, user_name, user_password):
        if (user_name == None) or (user_password == None):
            return False
        
        this.sql.execute(f"SELECT name FROM users WHERE name = '{user_name}'")
        if this.sql.fetchone() is None:
            this.sql.execute("INSERT INTO users VALUES (?,?)", (user_name, user_password))
            this.db.commit()
            # добавлен новый пользователь
        else:
            return Exception("user with this name already exists")
        
    def get_user_password(this, user_name):
        if (user_name == None):
            return False
        
        this.sql.execute("SELECT * FROM users WHERE name = ?", (user_name,) )
        return  UserInDB(this.sql.fetchone())

    def get_user(this, user_name):
        if (user_name == None):
            return None

        this.sql.execute("SELECT * FROM users WHERE name = ?", (user_name,) )
        return this.sql.fetchone()


    def getAllUsers(this):
        list_users = list()
        for value in this.sql.execute("SELECT * FROM users"):
            list_users.append(value)

        return list_users
    
    def delete(this):
        this.sql.execute("DROP TABLE IF EXISTS users")


all_users = UsersDB()

# print(all_users.create_user('Amir', 'ggggggs'))
# print(all_users.get_user("Amir"))

# print(all_users.getAllUsers())
# print(all_users.get_user_password('amir'))