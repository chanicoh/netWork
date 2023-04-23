from scapy.all import *

def ping(host):
    """
    Send an ICMP echo request to the specified host and wait for a response.
    Return True if the host responds, False otherwise.
    """
    icmp = ICMP()
    ip = IP(dst=host)
    packet = ip/icmp
    ping_responses = []
    for x in range(4):
      if packet is not None:
          ping_response = sr1(packet, timeout=2, verbose=0)

          ping_responses.append(ping_response)
    return ping_responses




def main():
    print(ping('www.google.com'))
if __name__ == '__main__':
    main()
