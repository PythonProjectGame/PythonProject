import pickle
import socket
import sqlite3
import bcrypt


host = "127.0.0.1"

port = 5555

s = socket.socket()
s.bind((host, port))

s.listen(10)

c, address = s.accept()
print(f"connected to {address}")


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
                return True
            else:
                return False

            conn.close()


while True:
    data = c.recv(1024)

    if not data:
        break

    data = pickle.loads(data)

    print(f"recieved {data}")

    print(sql(data))

    c.send(pickle.dumps(sql(data)))

c.close()
