"""EX 2.6 client implementation
   Author: chana cohen 935
   Date:
   Possible client commands defined in protocol.py
"""

import socket
import protocol

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        # 1. Add length field ("HELLO" -> "04HELLO")
        messege = protocol.create_msg(user_input)
        # 2. Send it to the server
        my_socket.send(messege.encode())
        # 3. Get server's response
        valid, data = protocol.get_msg(my_socket)
        # 4. If server's response is valid, print it
        if valid:
          if data != "EXIT":
             print("The server sent " + data)
            # 5. If command is EXIT, break from while loop
          else:
              break

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()
