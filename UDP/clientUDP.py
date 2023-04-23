from scapy.all import *
import socket

def split_data(data):
    data_split = []
    data_split[:] = data
    return data_split

def get_ascii_code(data_split):
    ascii_list = []
    for letter in data_split:
        ascii_letter = ord(letter)
        ascii_list.append(ascii_letter)
    return ascii_list

def making_socket():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return client

def make_packets(ascii_list):
    packets_list = []
    for letter in ascii_list:
        packet = IP(dst = '127.0.0.1')/UDP(dport = 8900, sport = 8900)/Raw(str(letter))
        packets_list.append(packet)
    last_char = get_ascii_code('.')
    last_packet = IP(dst = '127.0.0.1')/UDP(dport = 8900, sport = 8900)/Raw(str(last_char[0]))
    packets_list.append(last_packet)
    return packets_list

def send_packets(packets, client):
    for packet in packets:
        data = bytes(packet[Raw])
        clean_data = int(data)
        string_data = str(clean_data)
        print(string_data)
        client.sendto(string_data.encode(), ('127.0.0.1', 8900))

def main():
    data = input('What do you want to send? ')
    data_split = split_data(data)
    ascii_list = get_ascii_code(data_split)
    client = making_socket()
    packets = make_packets(ascii_list)
    send_packets(packets, client)

if __name__ == '__main__':
    main()