#!/usr/bin/python3
import seed


def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row[0]  # row is a tuple like (age,)

    cursor.close()
    connection.close()


def calculate_average_age():
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ 2nd (and final) loop
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")
