# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants
#                127.0.0.1
# TO DO: import modules
import socket
import os

# TO DO: set constants
IP = '0.0.0.0'
PORT = 80 #שרתי HTTP מקשיבים תמיד לPORT 80
SOCKET_TIMEOUT = 0.1
MAX_MSG_LENGTH = 1024

WEB_ROOT_LOCATION = r'C:\Networks\work\webroot{}'
DEFAULT_URL = '\index.html'
# region forbidden list and redirection dictionary for 302 codes
REDIRECTION_DICTIONARY = {'\mama': 'index.html'}
#FORBIDDEN_LIST = [""]
# endregion
FIXED_RESPONSE = ""
HTTP_VERSION = "HTTP/1.1 "
# Built in filed of Content
CONTENT_LENGTH_FILED = 'Content-Length: {}\r\n'
# region Status Codes
CODE_OK = '200 OK\r\n'
CODE_NOT_FOUND = '404 NOT Found\r\n\r\n'
CODE_Temporarily_Moved = "302 Found\r\nLocation: {}\r\n\r\n"
#CODE_FORBIDDEN = '403 Forbidden\r\n\r\n'
#CODE_INTERNAL_SERVER_ERROR = "500 Error Server Internal\r\n\r\n"


def get_file_data(filename):
    """ Get data from file """
    try:
        lines = ''
        with open(filename, 'rb') as my_file:
            lines = my_file.read()
        return lines
    except Exception:
        print("Fail to Get the data from:{}".format(filename))


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource
    print(resource)
    """אם זה 302 כלומר במשאב אוחלף"""
    if url in REDIRECTION_DICTIONARY.keys():
        # TO DO: send 302 redirection response
        http_response = HTTP_VERSION + CODE_Temporarily_Moved.format(REDIRECTION_DICTIONARY[url])
        client_socket.send(http_response.encode())

    # TO DO: 4.9 \calculate-area?height=2&width=2 i need to it
    elif '\\calculate-area' in resource:
        numbers = resource.split("?")[-1].split("&")
        height = ((numbers[0].split("="))[-1])
        length = ((numbers[1].split("="))[-1])
        if height.isdigit() and length.isdigit():
            height = int((numbers[0].split("="))[-1])
            length = int((numbers[1].split("="))[-1])
            print(str((height * length) / 2))
            http_header = "HTTP/1.1 200 OK Content type: text/plain\r\n\r\n" + str((height * length) / 2)
            client_socket.send(http_header.encode())
        else:
            http_header = "HTTP/1.1 200 OK Content type: text/plain\r\n\r\n" + "NaN"
            client_socket.send(http_header.encode())


    # send 404 not found
    elif not os.path.isfile(WEB_ROOT_LOCATION.format(url)):
        http_response = HTTP_VERSION + CODE_NOT_FOUND
        client_socket.send(http_response.encode())
    else:

        file_size = os.stat(WEB_ROOT_LOCATION.format(url)).st_size
        content_length = CONTENT_LENGTH_FILED.format(file_size)
        filetype = url[url.rfind('.') + 1::]
        prefix = HTTP_VERSION + CODE_OK + content_length
        # TO DO: extract requested file tupe from URL (html, jpg etc)
        if filetype == 'html' or filetype == 'txt':
            http_header = prefix + 'Content-Type: text/html; charset=utf-8\r\n\r\n'  # TO DO: generate proper HTTP header
        # TO DO: handle all other headers
        elif filetype == 'jpg':
            http_header = prefix + 'Content-Type: image/jpeg\r\n\r\n'
        elif filetype == 'js':
            http_header = prefix + 'Content-Type: text/javascript; charset=UTF-8\r\n\r\n'
        elif filetype == 'css':
            http_header = prefix + 'Content-Type: text/css\r\n\r\n'
        elif filetype == 'ico':
            http_header = prefix + 'Content-Type: image/vnd.microsoft.icon\r\n\r\n'
        elif filetype == 'gif':
            http_header = prefix + 'Content-Type: image/gif\r\n\r\n'
        filename = WEB_ROOT_LOCATION.format(url)
        # The Data from the file is not need to coded
        data = get_file_data(filename)
        print("I send file{}".format(filename))
        http_header = http_header.encode()
        http_response = http_header + data
        client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # First we will get the client request from all the data
    split_request = request.split("\n")[0].split(" ")   # ['GET', '/mama', 'HTTP/1.1\r']  ['GET', '/', 'HTTP/1.1\r']
    if split_request[1] == '/':
        return True, ''
    split_request[1] = split_request[1].replace('/', "\\")
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
                # 505 error
                #http_response = HTTP_VERSION + CODE_INTERNAL_SERVER_ERROR
                #client_socket.send(http_response.encode())
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