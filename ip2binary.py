#!/usr/bin/python

import sys
from netaddr import IPAddress as IP
if not len(sys.argv[1:]):
   print '\nUsage ip2binary.py 8.8.8.8'
   exit()


try:
   ip = IP(sys.argv[1])
   ip = ip.value
except:
   print 'Error with ip value'
   exit()

print
print 'IP:',IP(ip)
print 'Base2:', bin(ip)
print 'Base8:', oct(ip)
print 'Base10', ip
print 'Base16:', hex(ip)
print
