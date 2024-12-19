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
    """
    Process data from the server and return the result of the operation.

    Args:
        data (list): A list of values imputed from the server to make requests to the sql database

    Returns:
        str: The type of login required or the values from the game data
    """
    type = data[0]
    match type:
        case "Login":
            # Connect to the database
            conn = sqlite3.connect("GameData.db")
            cursor = conn.cursor()

            # Get the username and password from the data
            username, password = tuple(data[1:])

            # Check if the username exists in the database
            cursor.execute(
                f"select Password from LoginData where Username='{username}'"
            )

            try:
                # Get the password from the database
                pswd = cursor.fetchall()[0][0]
            except IndexError:
                # If the username does not exist, return False
                return "False"

            # Check if the password matches the one in the database
            if bcrypt.checkpw(password.encode(), pswd):
                # If the password matches, get the access right of the user
                cursor.execute(
                    f"select AccessRight from LoginData where Username='{username}'"
                )
                access = cursor.fetchall()[0][0]
                if access == "Admin":
                    # If the user is an admin, return Admin
                    return "Admin"
                else:
                    # If the user is a client, return Client
                    return "Client"
            else:
                # If the password does not match, return False
                return "False"

            # Close the database connection
            conn.close()

        case "Game":
            # Get the x and y coordinates from the data
            x, y = tuple(data[1:])


def threaded_client(conn: socket.socket) -> None:
    """
    Handle the client connection. This function will run in a separate thread.

    Args:
        conn: The address and port connection to the client
    """
    while True:
        # Recieve data from the client
        data: bytes = conn.recv(1024)

        if not data:
            continue

        # Convert the recieved data back to a list
        data: list = pickle.loads(data)

        print(f"recieved {data}")

        # If the client wants to exit, break the loop
        if data == "exit":
            break

        # Send the result of the operation back to the client
        conn.send(pickle.dumps(inputData(data)))


if __name__ == "__main__":
    while True:
        c, address = s.accept()
        print(f"connected to {address}")

        _thread.start_new_thread(threaded_client, (c,))

    c.close()
