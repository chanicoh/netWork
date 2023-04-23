import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"
# python c:\Networks\work\targil12.1\client12.1.py

def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind server socket to IP and Port
    server_socket.bind((SERVER_IP, SERVER_PORT))
    # Listen to incoming connections
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    #messages_to_send = []
    while True:
        read_list = client_sockets + [server_socket]
        ready_to_read, ready_to_write, in_error = select.select(read_list, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                client_socket, client_address = server_socket.accept()
                print("New client joined!\n", client_address)
                client_sockets.append(client_socket)
            else:
                data = current_socket.recv(MAX_MSG_LENGTH).decode()
                if data == "":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    print(data)
                    #messages_to_send.append((current_socket, data))
        """
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messages_to_send.remove(message)
        """

if __name__ == '__main__':
    main()