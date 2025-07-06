import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # add your password if needed
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row  # ✅ Yield one user at a time

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    batch = []
    for user in stream_users_in_batches(batch_size):
        if int(user['age']) > 25:
            batch.append(user)
        if len(batch) == batch_size:
            for u in batch:
                print(u)
            batch = []

    # Print any remaining users in the final incomplete batch
    if batch:
        for u in batch:
            print(u)

