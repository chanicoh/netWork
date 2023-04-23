from scapy.all import *
"""מדפיס את התחנות עד שמגיע לip הרצוי לדוג אני מקישה www.facebook.com הוא מדפיס את הIP עד שמגיע לIP הסופי """
#הפונקציה tracertמבוצע עם ping והוא עם ICMP
def get_address():
    dest_ip = input('What is the destination address? ')
    ttl = input('What is the ttl of the packet? ')
    return (dest_ip, ttl)

#מחזיר את החבילה
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
    print(
        'ID = ' + str(packet_id) + '\t\tIP = ' + str(packet_ip) + '\t\tTTL = ' + str(packet_ttl) + '\t\tTYPE = ' + str(
            packet_type))


def main():
    (dest_ip, ttl) = get_address()
    responses = []
    for packet_num in range(int(ttl)):
        ping_packet = build_packet(dest_ip, packet_num)
        ping_response = send_packet(ping_packet)
        response_type = ping_response[ICMP].type
        responses.append(ping_response)
        (packet_id, packet_ttl, packet_ip, packet_type) = get_data_from_response(ping_response, ttl, packet_num,
                                                                                 response_type)
        print_results(packet_id, packet_ttl, packet_ip, packet_type)

        if response_type == 0:
            print('Finished!!')
            break


if __name__ == "__main__":
    main()