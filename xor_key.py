#!/usr/bin/python

import sys
import string

outfile = False
hex_out = False
if not len(sys.argv[2:]):
   print """Usage:\t xor.py
		Input:  --rawfile <file> | --hexfile <file> | --string STRING | --inhex 50415353574F5244
		Key:    --key PASSWORD | --keyhex 50415353574F5244
		Output: --hex | --outfile <file>
"""
   exit()
if '--string' in sys.argv:
   string = sys.argv[sys.argv.index('--string')+1]
elif '--inhex' in sys.argv:
   string = sys.argv[sys.argv.index('--inhex')+1].decode('hex')
elif '--rawfile' in sys.argv:
   string = open(sys.argv[sys.argv.index('--rawfile')+1],'rb').read()
elif '--hexfile' in sys.argv:
   string = open(sys.argv[sys.argv.index('--hexfile')+1],'rb').read().replace('\n','').replace('\r','').replace(' ','').decode('hex')
else:
   print 'Missing input parameters...'
   exit()
if '--keyhex' in sys.argv[2:]:
   key = sys.argv[sys.argv.index('--keyhex')+1].decode('hex')
elif '--key' in sys.argv:
   key = sys.argv[sys.argv.index('--key')+1]
else:
   print 'Missing xor key...'
   exit()
if '--hex' in sys.argv:
   hex_out = True
elif '--outfile' in sys.argv:
   outfile = sys.argv[sys.argv.index('--outfile')+1]

#string = '''Burning 'em, if you ain't quick and nimble
#I go crazy when I hear a cymbal'''

cipher = []
cnt = 0
for c in string:
   cipher.append(chr(ord(c) ^ ord(key[cnt])))
   cnt += 1
   if cnt == len(key):
      cnt = 0

enc = ''.join(cipher)

if hex_out:
   print enc.encode('hex')
elif outfile:
   with open(outfile,'wb') as f:
     f.write(enc)
else:
   print enc
