import mysql.connector

mydb = mysql.connector.connect(
    host='localhost', user='proto', password='password', database='protodb')

mycursor = mydb.cursor()

createtable = "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"

sql = "INSERT INTO users (name,email,password) VALUES ('Johnathan','johnathan@email.com','john1234')"

selectsql = "SELECT * FROM users"
dropsql = "DROP TABLE users"

email = 'johnathan@email.com'
password = 'john1234'
selectlike = """SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(
    email, password)


# mycursor.execute(selectsql)
# # mydb.commit()
# print(mycursor.fetchall())
# print('query succesful')


def return_query(sql):
    mycursor.execute(sql)
    return mycursor.fetchone()


def commit_query(sql, val):
    mycursor.execute(sql, val)
    mydb.commit()
    return mycursor.fetchall()
