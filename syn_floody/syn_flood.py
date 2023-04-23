from scapy.all import *
from scapy.layers.inet import IP, TCP

#pcap
# Constants:
FILE_NAME = "C:\\Networks\\work\\syn_floody\\SYNflood.pcap"
ip_attack = "C:\\Networks\\work\\syn_floody\\write.txt"
# בחרתי ב 9 כי לדעתי מי ששולח הרבה syn ללא ack
# ייחשב כתוקף רק אם זה מעל 9 כי אולי הוא מזהה שלא קיבל syn ack לכן הוא שולח שוב
#תוקף ip  הוא מי ששלח לכתובת שמתחילה ב 100.65
LIMIT_TO_ATTACKERS = 9


def check_ip(pcapnpFile):
    """
    create a dictionary  all the IP addresses in the pcapng file,
    and for each IP address their value will be amount of occurrences,
    that they sent SYN flag without ACK flag.
    """
    # Dictionary for the ip addresses:
    suspected_ip = {}

    # Pass on all the packets in the pcapng file:
    for pkt in pcapnpFile:
         if pkt.haslayer(TCP) and IP in pkt:
             # filter to the ip the ip that send to  ip 100.64
             if pkt[IP].dst.startswith('100.64'):
                # If it is the first time we Encountered this IP address:
                if pkt[IP].src not in suspected_ip:
                   #  we put in out dictionary this IP address, and initializing her value to zero(0):
                   suspected_ip[pkt[IP].src] = 0

                 # if only the SYN flag is on:
                if pkt[TCP].flags == 'S':
                    # Then increase by one:
                     suspected_ip[pkt[IP].src] += 1

                # Else, if ACK flag is on:
                elif pkt[TCP].flags == 'A':
                    # If the amount of SYN occurrences is not zero:
                    if suspected_ip[pkt[IP].src] != 0:
                        # Then decrease by one:
                        suspected_ip[pkt[IP].src] -= 1

    return suspected_ip

def write_to_file(suspected_ip):
    """
     Run of all the dictionary keys,
    and write to 'write.txt' file all the suspect IP addresses (if they have more than 5 SYN without ACK).
    """
    with open(ip_attack, 'a') as write_file:
        # The amount of occurrences that the client sent SYN without ACK:
        count = 0
        # Run of all the dictionary keys:
        for ip in suspected_ip:
            # If the occurrences of SYN without ACK is more than 9:
            if suspected_ip[ip] > LIMIT_TO_ATTACKERS:
                count += 1
                # Write this IP address to the file:
                write_file.write(ip + '\n')

    print(count)


def main():
    # The pcapnp file:
    pcapnpFile = rdpcap(FILE_NAME)
    suspected_ip = check_ip(pcapnpFile)
    write_to_file(suspected_ip)


if __name__ == "__main__":
    main()