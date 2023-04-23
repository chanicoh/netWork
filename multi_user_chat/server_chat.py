import socket
import select
import protocol_chat
MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"

#   python c:\Networks\work\multi_user_chat\client_chat.py

#just msg from several
def create_server_rsp(cmd,div_client,from_client):# get client's choose,the dic, the address
    # check if user name exist
    if "MSG" in cmd and len(cmd.split())> 1:
        s = cmd.split()
        key = s[1]
        if key in div_client.keys():  # if not exist return error
            return "MSG"
        else:
            return "Username is not exist"
    # GET_NAMES will get all names
    elif cmd == "GET_NAMES":
        if div_client == {}:
            return "EMPTY"
        else:
            the_key = ""
            for i in div_client.keys():
                the_key += i +" "
            return the_key

    # NAME < name > will set name.Server will reply error if duplicate
    elif cmd[0:4:] == "NAME" and len(cmd.split())> 1:

        if from_client in div_client.values():
            return "You are already registered in the system"
        elif cmd[5::] in div_client.keys():  # if exist return error
            return "Username already exists"
        else:  # add to dic and return the message
            div_client[cmd[5::]] = from_client
            return "Hello " + cmd[5::]
    # client want to exit
    elif cmd == "EXIT":
        return "EXIT"
    else:
        return "NOT A VALID COMMENT"

# MSG < NAME > < message > will send message  to client name
def msg_to_clirnt(cmd):
    s = cmd.split()# for example ['MSG' , 'CHANA' , 'SHALOM']
    # creat the messege to send
    n = s[2]# msg
    for i in s[3:]:
        n = n + " " + i
    return n, s[1]#return the msg and for who the msg

#"get client and dic of client and remove the client if wand to exit"
def msg_exit(div_client,from_client):
    if from_client in div_client.values():
        for i in div_client.keys(): # i have the value and i have to find the key
            if div_client.get(i) == from_client:
                index = i
        del div_client[index]  # delete from dic



def main():
    print("Setting up server...")
    # Create TCP/IP socket object
    # my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind server socket to IP and Port
    server_socket.bind((SERVER_IP, SERVER_PORT))
    # Listen to incoming connections
    server_socket.listen()
    print("Listening for clients...")
    # the socket of client who join
    client_sockets = []
    messages_to_send = []
    div_client = {}#the name is the key
    # the tuple of the msg to send to client: (socket, msg)

    while True:
        read_list = client_sockets + [server_socket]
        rlist, wlist, in_error = select.select(read_list, client_sockets, [], 0.000001)
        for current_socket in rlist:
            if current_socket is server_socket:
                # Create client socket for incoming connection
                client_socket, client_address = current_socket.accept()
                print("New client joined!\n", client_address)
                client_sockets.append(client_socket)
            else:# creat a msg
                #data = current_socket.recv(MAX_MSG_LENGTH).decode()#לקרוא את המידע של הקלינט
                valid_msg, cmd = protocol_chat.get_msg(current_socket)
                print(cmd) #ptint to several the comment of client
                if valid_msg:
                    # If valid command - create response
                     response = create_server_rsp(cmd,div_client,current_socket)
                     if response == "EXIT":
                         #"if the client want ro exit i sent exit to the client because he have to close the socket of client" \
                          #"and i have to remove the socket from client_sockets "
                         print("Connection closed")
                         msg = protocol_chat.create_msg(response)
                         current_socket.send(msg.encode())
                         client_sockets.remove(current_socket)
                         msg_exit(div_client, current_socket)
                         current_socket.close()
                         msg_exit(div_client,current_socket)

                      # if client want to send msg to another client
                     #i get from functiy the name who get and i will send it to him"
                     elif response == "MSG":
                        msg_get, name_get = msg_to_clirnt(cmd)
                        socket_who_get = div_client.get(name_get)  # who have to get the msg
                        for i in div_client.keys():
                            if div_client.get(i) == current_socket:
                                the_sent = i #the name who send the msg
                        response1 = "Several send: "
                        response2 = " send "
                        print(response1 + the_sent + response2 + msg_get)
                        msg = protocol_chat.create_msg(response1 + the_sent + response2 + msg_get)
                        messages_to_send.append((socket_who_get, msg))  # add to tuple to write
                     else:
                        response1 = "Several send: "
                        print(response1 + response)
                        msg = protocol_chat.create_msg(response1 + response)
                        messages_to_send.append((current_socket, msg))
                else:
                    response = "Wrong protocol"
                    client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
               # chack if the client want to exit

            for message in messages_to_send:
                # "current_socket" is who have to get the msg "data" is the msg
                current_socket_msg, data_msg = message
                if current_socket in wlist:
                   current_socket_msg.send(data_msg.encode())
                   messages_to_send.remove(message)




if __name__ == '__main__':
    main()