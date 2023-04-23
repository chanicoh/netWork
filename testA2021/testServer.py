import testProtocol
#   python c:\Networks\work\testA2021\testClient.py
from scapy.all import *



def main():
    """"מקבלים כאן פקטות רק שהם ICMP ומוחזר TRUE כלומר מחרוזת תקינה"""
    p = sniff(count=1, lfilter=testProtocol.filter_msg)
    p[0].show()
    secret = p[0][Raw].load.decode()
    print("Secret message: " + secret)
    """כאן כבר זה התוצאה של המחרוזת שהקשנו"""
    result = testProtocol.calc(secret)
    dst = p[0][IP].src
    print(dst)
    res = testProtocol.create_msg(data=result, icmp_type=0, ip_dst=dst)
    res.show()
    """שולחים תפקטה שיצרנו עם הסוד"""
    send(res)
    print("Ack message: " + result)


if __name__ == '__main__':
    main()