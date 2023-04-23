import socket
import os
IP = '0.0.0.0'
PORT = 8200 #שרתי HTTP מקשיבים תמיד לPORT 80
SOCKET_TIMEOUT = 0.1
MAX_MSG_LENGTH = 1024
FIXED_RESPONSE = ""
HTTP_VERSION = "HTTP/1.1 "                                              # Built in filed of Content
CONTENT_LENGTH_FILED = 'Content-Length: {}\r\n'
DEFAULT_URL = "/"                                            # region Status Codes
CODE_OK = '200 OK\r\n'
CODE_NOT_FOUND = '404 NOT Found\r\n\r\n'
"""זה פיענוח פרוטוקול מיוחד ולפי זה אני שולחת תגובה"""

# 127.0.0.1:8200
#לדוגמא 127.0.0.1:8200/1/2/3


def special_protocol(url):
    if (url[0] != '/'):
        return False, ''
    request = url[1:]
    request = request.split('/')
    if len(request) != 3:
        return False, ''
    if not request[0].isdigit() or not request[1].isdigit() or not request[2].isdigit():
        return False, ''
    op = int(request[0])
    n1 = int(request[1])
    n2 = int(request[2])
    if op == 1:
        return True, str(n1 + n2)
    elif op == 2:
        return True, str(n1 - n2)
    elif op == 3:
        return True, str(n1 * n2)
    elif op == 4:
        if n2 == 0:
            return False, ''
        return True, str(n1 / n2)
    else:
        return False, ''


def handle_client_request(resource, client_socket):
    if resource == '/':
        url = DEFAULT_URL
    else:
        url = resource
    print(resource)
    # send 404 not found
    valid, data = special_protocol(url)
    if not valid:
        data = "ERROR"
        http_header = HTTP_VERSION + CODE_NOT_FOUND
    else:
        filetype = url[url.rfind('.') + 1::]
        http_header = HTTP_VERSION + CODE_OK + 'Content-Type: {}\r\n' f'Content-Length: {len(data)}\r\n\r\n'
        # TO DO: extract requested file tupe from URL (html, jpg etc)
        if filetype == 'html' or filetype == 'txt':
            http_header = http_header + 'Content-Type: text/html; charset=utf-8\r\n\r\n'  # TO DO: generate proper HTTP header
        # TO DO: handle all other headers
        elif filetype == 'jpg':
            http_header = http_header + 'Content-Type: image/jpeg\r\n\r\n'
        elif filetype == 'js':
            http_header = http_header + 'Content-Type: text/javascript; charset=UTF-8\r\n\r\n'
        elif filetype == 'css':
            http_header = http_header + 'Content-Type: text/css\r\n\r\n'
        elif filetype == 'ico':
            http_header = http_header + 'Content-Type: image/vnd.microsoft.icon\r\n\r\n'
        elif filetype == 'gif':
            http_header = http_header + 'Content-Type: image/gif\r\n\r\n'
        # The Data from the file is not need to coded
    client_socket.send(http_header.encode())
    client_socket.send(data.encode())


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # First we will get the client request from all the data
    split_request = request.split("\n")[0].split(" ")
    if split_request[0] == 'GET' and split_request[2] == "HTTP/1.1\r":
        return True, split_request[1]
    else:
        return False, 'ERROR'


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    client_socket.send(FIXED_RESPONSE.encode())

    while True:
        # TO DO: insert code that receives client request
        try:
            client_request = client_socket.recv(MAX_MSG_LENGTH).decode()
            valid_http, resource = validate_http_request(client_request)
            if valid_http:
                print('Got a valid HTTP request')
                handle_client_request(resource, client_socket)
                break
            else:
                print('Error: Not a valid HTTP request')
                break
        except Exception:
            break

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()