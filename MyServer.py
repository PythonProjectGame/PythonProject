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

s.listen(10)

def sql(data: list) -> bool:
    type = data[0]
    match type:
        case "Login":
            conn = sqlite3.connect("GameData.db")
            cursor = conn.cursor()

            username, password = tuple(data[1:])

            cursor.execute(f"select Password from LoginData where Username='{username}'")
            pswd = cursor.fetchall()[0][0]
            password = bcrypt.hashpw(password.encode(), pswd)
            if password == pswd:
                cursor.execute(f"select AccessRight from LoginData where Username='{username}'")
                access = cursor.fetchall()[0][0]
                if access == "Admin":
                    return "Admin"
                else:
                    return "Client"
            else:
                return "False"

            conn.close()

def threaded_client(conn):
    while True:
        data = conn.recv(1024)

        if not data:
            continue

        data = pickle.loads(data)

        print(f"recieved {data}")

        if data == "exit":
            break

        print(sql(data))

        conn.send(pickle.dumps(sql(data)))

while True:
    c, address = s.accept()
    print(f"connected to {address}")

    _thread.start_new_thread(threaded_client, (c))

c.close()
