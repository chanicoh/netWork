
def exp():
   ipee = "127.0.0.1:8153/reverce/198.58.118.167"
   #ב/ זה הבקשה ולכן הוא מחלק את זה לפיי /
   ipee1 ="127.0.0.1:8200/4/3/5"
   request = ipee1[1:]
   request = request.split('/')
   print(request)

"""הפונקציה כאן מ HTTP והא בודק את url שקיבל"""
def validate_http_request_http():
    request = 'GET /mama HTTP/1.1\r\nhost: 127.0.0.1\r'   #ככה ניראה מה שהפונקציה הזו מקבלת בעצם
    # First we will get the client request from all the data
    split_request = request.split("\n")[0].split(" ")
    if split_request[1] == '/':
        print(split_request[1])
    split_request[1] = split_request[1].replace('/', "\\")  #replace הכוונה להחליף אותו
    print(split_request)
    if split_request[0] == 'GET' and split_request[2] == "HTTP/1.1\r":
        return print(split_request[1])
    else:
        return print("ERROR")

"""הפונקציה כאן מ HTTP_dns אבל שונה  והוא בודק את url שקיבל"""
def validate_http_request_test():
    request = 'GET /1/4/3 HTTP/1.1\r\nhost: 127.0.0.1\r'
    # First we will get the client request from all the data
    split_request = request.split("\n")[0].split(" ")
    print(split_request)
    if split_request[0] == 'GET' and split_request[2] == "HTTP/1.1\r":
        return print(split_request[1])
    else:
        return print("ERROR")

def valid_port():
#למציאת פורטים פתוחים
    for port in range(20, 1025):
        syn_packet = IP(dst='192.168.1.1') / TCP(dport=port, seq=123, flags='S')
        syn_ack_packet = sr1(syn_packet, verbose=0, timeout=30)
        if syn_ack_packet:
            print(syn_ack_packet[TCP].sport)

def main():
   #exp()
   validate_http_request_http()


if __name__ == "__main__":
    main()