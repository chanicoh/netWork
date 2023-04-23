from sys import argv
import testProtocol
from scapy.all import *

def main():
    if len(sys.argv) == 1:
        print("No parameters were received")
        return
    """מרבלים כאן את הקלט הסודי מהסקריפת"""
    msg = argv[testProtocol.STR]
    print(f'Secret message: {msg}')
    my_packet = testProtocol.create_msg(data=msg, icmp_type=8) #8 אומר שזה בקשה
    # my_packet.show()
    send(my_packet)
    try:
        ans = sniff(count=1, lfilter=testProtocol.filter_msg, timeout=testProtocol.TIMEOUT)
        print(f'Ack message: {ans[0][Raw].load.decode()}')
    except:
        print('There is no answer')


if __name__ == '__main__':
    main()