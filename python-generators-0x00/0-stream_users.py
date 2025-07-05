import mysql.connector


def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="ashraf",
        password="123",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)  # Return rows as dictionaries
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
