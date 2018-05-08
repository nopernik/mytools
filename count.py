#!/usr/bin/python
import sys,re

W = '\033[0m'  # white (normal)
G = '\033[32m'  # green

if not len(sys.argv[2:]):
  print 'Usage: count.py STRING FILE [--hex] [--print]'
  exit(1)

with open(sys.argv[2],'rb') as fin:
  f = fin.read()

def FindOffsets(target, match):
   #print 'Regex find: %r in %r' % (match,target)
   return [m.start() for m in re.finditer('(?={})'.format(re.escape(match)), target)]

prn = False
if '--print' in sys.argv:
  prn = True

hexa = False
if '--hex' in sys.argv:
  hexa = True

if hexa:
  match = sys.argv[1].decode('hex')
else:
  match = sys.argv[1]

offsets = FindOffsets(f,match)
for offset in offsets:
  out = 'Found'
  if prn:
    if hexa:
       out = f[offset-8:offset].encode('hex')+G+f[offset:offset+len(match)].encode('hex')+W+f[offset+len(match):offset+len(match)+8].encode('hex')
    else:
       out = f[offset-8:offset]+G+f[offset:offset+len(match)]+W+f[offset+len(match):offset+len(match)+8]
    print '0x%08x: %s' % (offset,out)
  else:
    print '0x%08x' % offset
