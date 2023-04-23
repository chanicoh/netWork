from scapy.all import *

STR = 1
TIMEOUT = 10
ERROR_MESSAGE = 'Error - Division by 0 is impossible'

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

"""כאן מקבלים את הפקטה ורצים רק על פקטות שהם ICMP ובודקים אם המחרוזת תקינה אז מחזירים TRUE"""
def filter_msg(my_packet):
    if ICMP in my_packet and Raw in my_packet:
        msg = str(my_packet[Raw].load.decode())
        if (my_packet[ICMP].type == 8) and (len(msg) == 9) and (msg[:-1].isdigit()) and (msg[-1] in ops):
            # print('filter_message(my_packet) => True')
            return True
        """0 הכוונה שזה מענה לבקזה ששלחנו ו8 זה בקשה """
        if (my_packet[ICMP].type == 0) and ((is_float(msg)) or (msg == ERROR_MESSAGE)):
            # print('filter_message(my_packet) => True')
            return True
    # print('filter_message(my_packet) => False')
    return False

""""יוצר את המספר הסודי לפי מה שקיבלנו ומחזיר את המספר במחרוזת"""
def calc(secret):
    part1 = int(secret[:4])
    part2 = int(secret[4:8])
    operation = secret[8]
    if operation == '/' and part2 == 0:
        return ERROR_MESSAGE
    return str(ops[operation](part1, part2))

"""מקבל את המספר הסודי ומחזיר פקטה """
def create_msg(data, icmp_type, ip_dst='127.0.0.1'):
    print(f'icmp type: {icmp_type}')
    return IP(dst=ip_dst) / ICMP(type=icmp_type) / Raw(load=data)