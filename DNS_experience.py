from scapy.layers.dns import *
from scapy.all import*
import sys
   #opcode=0 הכוונה שאילה סטנדרטית
"""מפלטר פקטות לפי שהם DNS וסוג ומדפיס שם"""
def dns_filter(pack):
    if (DNS in pack) and (DNSQR in pack):
        return (pack[DNS].opcode == 0) and (pack[DNSQR].qtype == 1)


def print_qname(pack):
    print(pack[DNSQR].qname.decode())

"""בגלל ש scapy לא מכיר את פקוטוקול HTTP אז אפשר לבדוק אם מתחיל ב GET וככה לסנן פקטות"""
def http_get_filter(packet):
  return (TCP in packet and Raw in packet and str(packet[Raw]).startswith('GET'))


#  python c:\Networks\work\DNS_experience.py www.jct.ac.il
"""מדפיס את התחנות של הכתובת כמו Tracert"""
def print_station():

    destination = "www.jct.ac.il" #פרמטר סקיפט שמקבלים בשלור

    i=1
    while True:
       packet = IP(ttl=i, dst=destination) / ICMP()
       try:
         res = sr1(packet,verbose=0,timeout=2)
         print(res[IP].src)
         if res[ICMP].type ==0:
            break
         i += 1
       except:
         continue



def main():
    destination = "www.facebook.com"
    #sniff(count=6, lfilter=dns_filter, prn=print_qname)
    print_station()




if __name__ == "__main__":
     main()