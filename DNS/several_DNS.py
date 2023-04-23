from scapy.all import *
i, o, e = sys.stdin, sys.stdout, sys.stderr
sys.stdin, sys.stdout, sys.stderr = i, o, e
SERVER_IP = '0.0.0.0'
PORT = 8153
SOCKET_TIMEPUT = 2
BUCKET = 1024
HTTP_KEY_WORDS = ["GET", "HTTP/1.1"]
HTTP_VERSION = 'HTTP/1.1'
CODE_OK = "HTTP/1.0 200 OK\r\n"
#
# 127.0.0.1:8153/www.youtube.com

def create_packet(ip_addr, dns_type):
    if dns_type is None:
        """כאן מדובר בסוג A ,המתאר רשומה הממפה בין שם דומיין לכתובת IP """
        dns_type = 'A'    
    dns_packet = IP(dst='8.8.8.8') / UDP(sport=24601, dport=53)
    dns_packet = dns_packet / DNS(qdcount=1, rd=1) / DNSQR(qname=ip_addr, qtype=dns_type)
    try:
        responsePacket = sr1(dns_packet, verbose=0, timeout=SOCKET_TIMEPUT)
    except():
        responsePacket = None
    return dns_packet


def extract_type_a(ip_addr, pkt):
    # return list of ip
    responses = []
    for p in pkt:
        if p.haslayer(DNSRR):
            for index in range(p[1][DNS].ancount):
                responses.append(p[DNSRR][index].rdata)
    try:
        reply = '\r\n            '.join(responses)
    except TypeError:
        for response in responses:
            if isinstance(response, bytes):
                responses.remove(response)
        reply = '\r\n            '.join(responses)
    return "Name:       " + ip_addr + "\nAddresses:  " + reply


def correctIp(ipcur):
    """to check is it is currect ip """
    adress = ipcur.split('.')
    if len(adress) == 4:
        for num in adress:
            if not (num.isdigit() and int(num) in range(0, 257)):
                return False
        return True
    else:
        return False

def extract_type_ptr(ip_addr, pkt):
    lst = ip_addr.split('.')
    lst.remove('in-addr')
    lst.remove('arpa')
    lst.reverse()
    ip_addr = '.'.join(lst)
    domain_name = ''
    try:
        domain_name = pkt[1].ns.rname
    except AttributeError:
        try:
            domain_name = pkt[1][DNSRR].rdata
        except TypeError:
            pass
    if isinstance(domain_name, bytes):
        domain_name = domain_name.decode("utf-8")
    if domain_name.endswith('.'):
        domain_name = domain_name[:-1]
    return "Name:       " + domain_name + "\nAddresses:  " + ip_addr


def handle_packet(ip_addr, dns_type):
    response_packets, unanswered_packets = sr(create_packet(ip_addr, dns_type), verbose=0)
    response = ''
    if dns_type == 'A':
        for pkt in response_packets:
            response = response + extract_type_a(ip_addr, pkt)
    else:
        for pkt in response_packets:
            response = response + extract_type_ptr(ip_addr, pkt)
    return response


def handle_client_dns(request, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    response = ''
    ip_rec = request.split('/')
    lengthR = len(ip_rec)
    questionName = ip_rec[lengthR - 1]
    if request.startswith('/reverse'):
        """if the ip not currect"""
        cut_ip =correctIp(questionName)
        if not cut_ip:
            data = "The IP address is invalid"
            http_header = HTTP_VERSION + ' 500 Internal Server Error \r\n\r\n ' +data
        else:
            ip = request[9:].split('.')
            ip.reverse()
            ip_address = '.'.join(ip) + ".in-addr.arpa"
            """if the network is not working"""
            response_pa = create_packet(ip_address, "PTR")
            if not response_pa:
                data = "the network is not working"
                print("the network is not working")
                http_header = HTTP_VERSION + ' 500 Internal Server Error \r\n\r\n ' + data
            else:
               response = handle_packet(ip_address, "PTR")
               http_header = HTTP_VERSION + CODE_OK + "Content-Length: " + str(len(response)) + "\r\n\r\n" + response
    else:

        url = request[1:]
        response_pa = create_packet(url, "A")
        """if the network is not working"""
        if not response_pa:
            data = "the network is not working"
            print("the network is not working")
            http_header = HTTP_VERSION + ' 500 Internal Server Error \r\n\r\n ' + data
        else:
           response = handle_packet(url, "A")
           http_header = HTTP_VERSION + CODE_OK + "Content-Length: " + str(len(response)) + "\r\n\r\n" + response
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