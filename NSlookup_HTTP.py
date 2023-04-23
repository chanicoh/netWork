
from scapy.all import *
i, o, e = sys.stdin, sys.stdout, sys.stderr
sys.stdin, sys.stdout, sys.stderr = i, o, e
SERVER_IP = '0.0.0.0'
PORT = 8153
SOCKET_TIMEPUT = 20
BUCKET = 1024
HTTP_KEY_WORDS = ["GET", "HTTP/1.1"]
HTTP_VERSION = 'HTTP/1.1'
CODE_OK = "HTTP/1.0 200 OK\r\n"
# 127.0.0.1:8153/www.youtube.com
# 127.0.0.1:8153
#לדוגמא 127.0.0.1/8153/
#/www.jct.ac.il
def get_ip_addr(domain_name):
    """
    Given a domain name, resolves it to an IP address using the scapy library.If the domain name is not valid, returns an appropriate error message.
    If the domain name corresponds to a client connected to the server, returns the client's IP address
    :param domain_name: a domain name or one of the client's names
    :return: the domains / clients ip addresses
    """
    data = ''
    # creating a scapy packet
    dns_packet = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(qdcount=1, rd=1, qd=DNSQR(qname=domain_name))
    # creating a scapy packet
    response_packet = sr1(dns_packet, verbose=0, timeout=3)  # sending packet and receiving first response
    if response_packet is None:  # the time passed but still no response
        return 'please check your internet connection'
    count = response_packet[DNS].ancount  # looking for amount of ip addresses
    if count == 0:  # there's a response, but no ip addresses
        return 'Wrong domain, please check your spelling'
    for i in range(count):
        if response_packet[DNSRR][i].type == 1:  # type == 'A' is an ip address
            data += response_packet[DNSRR][i].rdata + '\n'
    return data

def nslookup(url):
    if (url[0] != '/'):
        return False, ''
    request = url[1:]
    request = request.split('/')
    if len(request) != 1:
        return False, ''
    return str(get_ip_addr(request[0]))

def build_packet(dst_ip, ttl):
    ping_packet = IP(dst=dst_ip, ttl=int(ttl + 1)) / ICMP(type='echo-request')
    return ping_packet

def handle_client_dns(url, client_socket):
    request = url[1:]
    request = request.split('/')
    if len(request) != 2:
        return False, ''
    dest_ip = request[0]
    print("address: "+dest_ip)
    ttl = request[1]
    responses = []
    for packet_num in range(int(ttl)):
        ping_packet = build_packet(dest_ip, packet_num)
        ping_response = send_packet(ping_packet)
        response_type = ping_response[ICMP].type
        responses.append(ping_response)
        (packet_id, packet_ttl, packet_ip, packet_type) = get_data_from_response(ping_response, ttl, packet_num, response_type)
        result = print_results(packet_id, packet_ttl, packet_ip, packet_type)
    http_header = HTTP_VERSION + CODE_OK + "Content-Length: " + str(len(result)) + "\r\n\r\n" +result
    client_socket.send(http_header.encode())
    return

"""בודק שURL שמקבל תקין"""
def valid_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    parts = request.split()
    if parts[0] == HTTP_KEY_WORDS[0] and parts[2] == HTTP_KEY_WORDS[1]:
        return True, parts[1]
    else:
        return False, None


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')

    while True:
        # insert code that receives client request
        client_request = client_socket.recv(BUCKET).decode()
        valid_http, request = valid_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_dns(request, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            http_header = "HTTP/1.0 500 Internal Server Error\r\n"
            client_socket.send(http_header.encode())
            break

    print('Closing connection')
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEPUT)
        handle_client(client_socket)


if __name__ == "__main__":
    main()