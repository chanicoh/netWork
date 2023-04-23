"""EX 2.6 server implementation
   Author:
   Date:
   Possible client commands defined in protocol.py
"""
# python c:\Networks\work\targil2\client26.py
import socket
import protocol
from datetime import datetime
import random

MAX_RAND_INT = 99
IP = '0.0.0.0'


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    #server should reply with time and date
    if cmd == "TIME":
        now = datetime.now()
        return now.strftime("%m/%d/%y,%H:%M:%S")
    #server should reply with a random number, 0-99
    elif cmd == "NUMBER":
        return str(random.randint(1, MAX_RAND_INT))
    #server should reply with the server's name, anything you want
    elif cmd == "HELLO":
        return "HELLO SERVER"
    #erver should send acknowledge and quit
    elif cmd == "EXIT":
        return "EXIT"


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g NUMBER, HELLO, TIME, EXIT)"""
    if data in ["NUMBER", "HELLO", "TIME","EXIT"]:
      return True
    else:
        return False


def main():
    # Create TCP/IP socket object
    #my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_server = socket.socket()
    # Bind server socket to IP and Port
    my_server.bind((IP, protocol.PORT))
    # Listen to incoming connections
    my_server.listen()

    print("Server is up and running")
    # Create client socket for incoming connection
    (client_socket, client_address) = my_server.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print(cmd)
            # 2. Check if the command is valid, use "check_cmd" function
            if check_cmd(cmd):
            # 3. If valid command - create response
                 response = create_server_rsp(cmd)
            else:
                response = "Wrong protocol"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        # Send response to the client
        client_socket.send(protocol.create_msg(response).encode())
        # If EXIT command, break from loop
        if response == "EXIT":
           break

    print("Closing\n")
    # Close sockets
    my_server.close()
    client_socket.close()

if __name__ == "__main__":
    main()
