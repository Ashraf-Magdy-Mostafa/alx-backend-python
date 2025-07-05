import mysql.connector


def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",
        password="your_mysql_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)  # Return rows as dictionaries
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
