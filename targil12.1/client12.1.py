import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5555))
msg = input("Pls enter message\n")
while msg != "EXIT":
    my_socket.send(msg.encode())
    #data = my_socket.recv(1024).decode()
    #print("Server replied:", data)
    msg = input("Pls enter message\n")

my_socket.close()

