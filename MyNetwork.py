import socket
import pickle
import pygame

pygame.init()


host = "127.0.0.1"
port = 5555

client_socket = socket.socket()

client_socket.connect((host, port))
data = input()


while data != "bye":
    data = pickle.dumps(data)
    client_socket.send(data)
    indata = client_socket.recv(1024)
    indata = pickle.loads(indata)
    print(indata)
    data = input()


client_socket.close()
