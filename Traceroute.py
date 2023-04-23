from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import scapy.config
import sys
"""עושה Traceroute מדפיס את התחנות בינינו לבין הכתובת הרצויה"""

#           python c:\Networks\work\Traceroute.py www.facebook.com
def main(ip):
	req = IP(ttl=1,dst=ip)/ICMP()
	res = sr1(req,verbose=0,timeout=1)
	print("1",res[IP].src,(res.time-req.time)*1000, "ms")
	i = 2
	while res[IP].src != req[IP].dst:
		req = IP(ttl=i,dst=ip)/ICMP()
		res = sr1(req,verbose=0,timeout=1)
		if res is not None:
			print(i,res[IP].src,(res.time-req.time)*1000, "ms")
		else:
			break




		i+=1

if __name__ == "__main__":
	#if (len(sys.argv) == 2):
	#	main(sys.argv[1])
	main("www.facebook.com")
