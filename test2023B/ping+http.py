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
# 127.0.0.1:8153/ping/www.facebook.com/4
#  127.0.0.1:8153/ARP/192.168.1.1"


""" A function that builds the package and return the list of the ip """
def build_packet_ping(dst_ip,count):
    packet = IP(dst=dst_ip) / ICMP()
    ping_responses = []
    for ipd in range(int(count)):
        if packet is not None:
            ping_response = sr1(packet, timeout=2, verbose=0)
            ping_responses.append(ping_response.summary())
    return ping_responses

def find_mac_address(ip):
    # Create an ARP request packet to get the MAC address of the IP
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    # Send the packet and capture the response
    result = srp(packet, timeout=3, verbose=0)[0]
    # Extract and return the MAC address from the response
    return result[0][1].hwsrc


def handle_client_request(url, client_socket):
    """Receives the coagulation as well as an IP address or address and returns according to the requirements"""
    request = url[1:]
    request = request.split('/')
    dest_ip = request[1]
    theAs=request[0]
    if theAs=="ping":
      theCo =request[2]
      print("address: "+dest_ip)
      responses = build_packet_ping(dest_ip,theCo)
      stringrespon = ' \n'.join(str(x) for x in responses)
      http_header = HTTP_VERSION + CODE_OK + "Content-Length: " + str(len(stringrespon)) + "\r\n\r\n" +stringrespon
      client_socket.send(http_header.encode())

    if theAs=="ARP":
        macAddress = find_mac_address(dest_ip)
        print(macAddress)
        mac = macAddress
        http_header = HTTP_VERSION + CODE_OK + "Content-Length: " + str(len(mac)) + "\r\n\r\n" + mac
        client_socket.send(http_header.encode())
    return



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
        try:
          client_request = client_socket.recv(BUCKET).decode()
          valid_http, request = valid_request(client_request)
          if valid_http:
              print('Got a valid HTTP request')
              handle_client_request(request, client_socket)
              break
          else:
              print('Error: Not a valid HTTP request')
              http_header = "HTTP/1.0 500 Internal Server Error\r\n"
              client_socket.send(http_header.encode())
              break
        except Exception:
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