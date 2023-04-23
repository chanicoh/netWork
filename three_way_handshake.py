from scapy.all import *

def make_packet():
    syn_segment = TCP(dport = 80, seq = 123, flags = 'S')
    syn_packet = IP(dst = 'www.google.com')/syn_segment
    return syn_packet


def send_packets(syn_packet):
    response = sr1(syn_packet)
    response_ack = response[TCP].ack
    response_seq =response[TCP].seq
    return response, response_ack, response_seq


def make_ack_packet(syn_packet, response, response_ack, response_seq):
    ack_packet = IP(dst = 'www.google.com')/TCP(dport = 80, seq = response_ack, ack = (response_seq + 1), flags = 'A')
    return ack_packet

def send_ack_packet(ack_packet):
    response = send(ack_packet)
    return response

def main():
    syn_packet = make_packet()
    response, response_ack, response_seq = send_packets(syn_packet)
    ack_packet = make_ack_packet(syn_packet, response, response_ack, response_seq)
    ack_response = send_ack_packet(ack_packet)
    print(ack_packet.show())

if __name__ == '__main__':
    main()