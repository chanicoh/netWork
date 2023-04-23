from scapy.all import *
  #python c:\Networks\work\test2023A\test_now.py
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
import sys

i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *

sys.stdin, sys.stdout, sys.stderr = i, o, e


def read_args():
    parameters = []
    if len(sys.argv) == 2:
        return sys.argv[0], sys.argv[1]
    for arg in sys.argv:
        parameters.append(arg)
    return parameters


def create_packet(ip_addr, dns_type):
    if dns_type is None:
        dns_type = 'A'
    my_packet = IP(dst='8.8.8.8') / UDP(sport=24601, dport=53) / \
                DNS(qdcount=1, rd=1) / DNSQR(qname=ip_addr, qtype=dns_type)
    return my_packet


def extract_type_a(ip_addr, pkts):
    responses = []
    try:
        for p in pkts:
            if p.haslayer(DNSRR):
                for index in range(p[DNS].ancount):
                    responses.append(p[DNSRR][index].rdata)
        reply = '\r\n            '.join(responses)
    except AttributeError:
        for pkt in pkts:
            for p in pkt:
                if p.haslayer(DNSRR):
                    for index in range(p[DNS].ancount):
                        responses.append(p[DNSRR][index].rdata)
        reply = '\r\n            '.join(responses)
    return "Name:       " + ip_addr + "\nAddresses:  " + reply


def extract_type_ptr(ip_addr, pkts):
    domain_name = ''
    for pkt in pkts:
        lst = ip_addr.split('.')
        lst.remove('in-addr')
        lst.remove('arpa')
        ip_addr = '.'.join(lst)
        domain_name = ''
        try:
            domain_name = pkt.ns.rname
        except Exception:
            pass
        try:
            domain_name = pkt[DNSRR].rdata
        except Exception:
            pass
        if domain_name.endswith(b'.'):
            domain_name = domain_name[:-1]
    return "Name:       " + domain_name.decode("utf-8") + "\nAddresses:  " + ip_addr


def handle_packet(ip_addr, dns_type):
    response_packets = sr(create_packet(ip_addr, dns_type))
    response = ''
    if dns_type == 'A':
        response = extract_type_a(ip_addr, response_packets)
    else:
        response = extract_type_ptr(ip_addr, response_packets)
    print(response)
    return


def main():
    params = 'www.youtube.com'
    ip_address = None
    dns_type = None
    if len(params) == 2:
        ip_address = params[1]
        dns_type = 'A'
    elif len(params) == 3:
        if params[1] == "-type=PTR" or params[1] == "-type=ptr":
            ip = params[2].split('.')
            ip.reverse()
            ip_address = '.'.join(ip) + ".in-addr.arpa"
            dns_type = "PTR"
    handle_packet(ip_address, dns_type)


if __name__ == "__main__":
    main()