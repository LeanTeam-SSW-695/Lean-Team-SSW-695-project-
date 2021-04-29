import mysql.connector
from mysql.connector.constants import ClientFlag

def set_connection:
    config = {
        'user': 'root',
        'host': '35.220.246.119',
        'password': "12345678",
        'client_flags': [ClientFlag.SSL]
    }
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()  # initialize connection cursor
def create_table:
    set_connection()
    try:
        cursor.execute('CREATE DATABASE login')  # create a new 'testdb' database
        cnxn.close()
        config['database'] = 'login'  # add new database to config dict
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()
        cursor.execute("CREATE TABLE space_missions ("
                       "Username VARCHAR(255),"
                       "Pwd VARCHAR(255) )")

        cnxn.commit()  # this commits changes to the database
    except:
        print("Database exists")

def register(username, pwd):
    set_connection()
    if login(username, pwd):
        print("User has registered!")
        return False
    cursor.execute("SELECT COUNT(*) FROM login WHERE Username = '" + username+ "'")
    out = cursor.fetchall()
    if out[0][0]:
        print("Username has been used!")
    else:
        query = "INSERT INTO login (Username, Pwd) VALUES ('" + username + "', '" + pwd + "')"
        cursor.execute(query)
        cnxn.commit()  # and commit changes
        return True

def login(username, pwd):
    set_connection()
    query = "SELECT COUNT(*) FROM login WHERE Username = '" + username + "' AND Pwd = '" + pwd + "'"
    cursor.execute(query)
    out = cursor.fetchall()
    if out[0][0]:
        return True
    else:
        return False
