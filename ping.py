from scapy.all import *

#python c:\Networks\work\ping.py www.facebook.com
def get_address():
    dest_ip ="www.facebook.com"
        #= input('What is the destination address? ')
    return dest_ip


def build_packet(dst_ip):
    ping_packet = IP(dst = dst_ip)/ICMP(type = 'echo-request')
    return ping_packet

def send_packet(ping_packet):
    ping_responses = []
    for x in range(5):
        ping_response = sr1(ping_packet)
        ping_responses.append(ping_response)
    return ping_responses

def show_responses(ping_responses):
    for packet in ping_responses:
        print(packet.summary())

def main():
    dest_ip = get_address()
    ping_packet = build_packet(dest_ip)
    ping_responses = send_packet(ping_packet)
    show_responses(ping_responses)

if __name__ == '__main__':
    main()
