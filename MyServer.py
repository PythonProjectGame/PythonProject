import pickle
import socket
import sqlite3
import bcrypt
import _thread


host = "127.0.0.1"

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    str(e)

s.listen()


def inputData(data: list) -> any:
    """_summary_

    Args:
        data (list): A list of values imputed from the server to make requests to the sql database

    Returns:
        str: The type of login required or the values from the game data
    """
    type = data[0]
    match type:
        case "Login":
            conn = sqlite3.connect("GameData.db")
            cursor = conn.cursor()

            username, password = tuple(data[1:])

            cursor.execute(
                f"select Password from LoginData where Username='{username}'"
            )
            try:
                pswd = cursor.fetchall()[0][0]
            except IndexError:
                return "False"

            if bcrypt.checkpw(password.encode(), pswd):
                cursor.execute(
                    f"select AccessRight from LoginData where Username='{username}'"
                )
                access = cursor.fetchall()[0][0]
                if access == "Admin":
                    return "Admin"
                else:
                    return "Client"
            else:
                return "False"

            conn.close()

        case "Game":
            x, y = tuple(data[1:])


def threaded_client(conn):
    """_summary_

    Args:
        conn: The address and port connection to the client
    """
    while True:
        data = conn.recv(1024)

        if not data:
            continue

        data = pickle.loads(data)

        print(f"recieved {data}")

        if data == "exit":
            break

        conn.send(pickle.dumps(inputData(data)))


if __name__ == "__main__":
    while True:
        c, address = s.accept()
        print(f"connected to {address}")

        _thread.start_new_thread(threaded_client, (c,))

    c.close()
