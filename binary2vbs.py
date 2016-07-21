#!/usr/bin/python
#__author__ @nopernik

import sys

header = '''Function myWrite(data)
        For i = 1 to Len(data) Step 2
            myFile.Write Chr(CLng("&H" & Mid(data,i,2)))
        Next
End Function

Dim myArray

myArray = Array( _'''

footer = '''
Dim fObject
Set fObject = CreateObject("Scripting.FileSystemObject")
Dim myFile
Dim fileName
fileName = "binary.bin.js"
Set myFile = fObject.CreateTextFile(fileName, true , false)

For each i in myArray
    myWrite(i)
Next

myFile.Close
'''

if not len(sys.argv[1:]):
	print 'Usage: binary2vbs file'
	exit()

f = open(sys.argv[1],'rb')
infile = f.read()
f.close()

line = infile.encode('hex')

for i in range(200,300,2):
	if len(line) % i != 0:
		n = i
		break

print header

for b in [line[i:i+n] for i in range(0, len(line), n)]: 
	if not len(b) < n:
		print '"%s", _' % b
	else:
		print '"%s")' % b

print footer
