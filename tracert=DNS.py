from scapy.all import *
i, o, e = sys.stdin, sys.stdout, sys.stderr
sys.stdin, sys.stdout, sys.stderr = i, o, e
SERVER_IP = '0.0.0.0'
PORT = 8153
SOCKET_TIMEPUT = 0.1
BUCKET = 1024
HTTP_KEY_WORDS = ["GET", "HTTP/1.1"]
HTTP_VERSION = 'HTTP/1.1'
CODE_OK = "HTTP/1.0 200 OK\r\n"
# 127.0.0.1:8153/www.youtube.com
def build_packet(dst_ip, ttl):
    ping_packet = IP(dst=dst_ip, ttl=int(ttl + 1)) / ICMP(type='echo-request')
    return ping_packet


def send_packet(ping_packet):
    ping_response = sr1(ping_packet, verbose=0)
    return ping_response


def get_data_from_response(response, ttl, packet_num, response_type):
    packet_ttl = (int(ttl) - (packet_num + 1))
    packet_id = packet_num + 1
    packet_ip = response[IP].src
    packet_type = response_type
    return (packet_id, packet_ttl, packet_ip, packet_type)

def print_results(packet_id, packet_ttl, packet_ip, packet_type):
    return (
        'ID = ' + str(packet_id) + '\t\tIP = ' + str(packet_ip) + '\t\tTTL = ' + str(packet_ttl) + '\t\tTYPE = ' + str(  packet_type))



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
        (packet_id, packet_ttl, packet_ip, packet_type) = get_data_from_response(ping_response, ttl, packet_num, response_type)
        result = print_results(packet_id, packet_ttl, packet_ip, packet_type)
        responses.append(result)
    stringrespon = ' \n'.join(str(x) for x in responses)
    http_header = HTTP_VERSION + CODE_OK + "Content-Length: " + str(len(stringrespon)) + "\r\n\r\n" +stringrespon
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