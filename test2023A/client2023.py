
# NAME <name> will set name. Server will reply error if duplicate
# GET_NAMES will get all names
# MSG <NAME> <message> will send message to client name
# EXIT will close client
# python c:\Networks\work\test2023A\client2023.py
import socket
import msvcrt
import select
import protocol2023



def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", 5555))
    "rlist is to read the msg from server"

    # 1. enter comment
    commend = ""
    print("WELCOME\n")
    while True:
        rlist, wlist, xlist = select.select([my_socket], [], [], 0.000001)
        if my_socket in rlist:
            # get respone from several
            valid, data = protocol2023.get_msg(my_socket)
            if valid:
                if data == "EXIT":
                    break
                else:
                    print(data)

        if msvcrt.kbhit():
            key = msvcrt.getch().decode()
            if key == '\r':# this ent of msg
                print(key, flush=True)
                # create a msg
                msg = protocol2023.create_msg(commend)
                # 3. Send it to the server
                my_socket.send(msg.encode())
                commend = ""
                # 4. Get server's response
            else:
                print(key, end="", flush=True)  # print in wan line
                commend += key





if __name__ == "__main__":
    main()