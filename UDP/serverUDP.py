from scapy.all import *
import socket

#  python c:\Networks\work\UDP\clientUDP.py


def initialize_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', 8900))
    print('Server is up and ready!!')
    return server

def recv_ports(server):
    data = 0
    numbers_list = []
    while data != '46':
        (client, client_address) = server.recvfrom(1024)
        data = client.decode()
        numbers_list.append(data)
    return client, client_address, numbers_list

def decode_data(data):
    decoded_list = []
    for number in data:
        letter = chr(int(number))
        decoded_list.append(letter)
    return decoded_list

def merge_data(decoded_data):
    response = ''.join(decoded_data)
    return response

def main():
    server = initialize_server()
    (client, client_address, data_list) = recv_ports(server)
    decoded_data = decode_data(data_list)
    response = merge_data(decoded_data)
    print(response)
if __name__ == '__main__':
    main()