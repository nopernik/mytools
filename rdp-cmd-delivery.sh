#!/bin/bash

# by @nopernik
#
# dependency xdotool

WINDOWNAME=rdesktop

if [ -z $1 ]; then
   echo -e "\nUsage: rdp-cmd-delivery.sh OPTIONS file.ps1\n"
   echo -e "        OPTIONS:"
   echo    "                 --tofile 'c:\test.txt' local.ps1 #will copy contents of local.ps1 to c:\test.txt"
   echo    "                 --cmdfile local.bat                #will execute everything from local.bat"
   echo
   echo -e "        To deliver powershell payload, use '--cmdfile script.ps1' but inside powershell console\n"
   exit 1
fi

function catFile {
  # $1 localfile content
  xdotool search --name $WINDOWNAME windowfocus windowactivate type "$1"
  xdotool search --name $WINDOWNAME windowfocus windowactivate key Return
}

function copyCon {
  # $1 = filename to create remotely
  # $2 = file content
  xdotool search --name $WINDOWNAME windowfocus windowactivate type "copy con $1"
  xdotool search --name $WINDOWNAME windowfocus windowactivate key Return
  xdotool search --name $WINDOWNAME windowfocus windowactivate type "$2"
  xdotool search --name $WINDOWNAME windowfocus windowactivate key Ctrl+Z Return
}

if [ "$1" = "--cmdfile" ]; then
  catFile "$(cat $2)"
  exit 0
fi

if [ "$1" = "--tofile" ]; then
  if [ ! -z "$3" ];then
    copyCon "$2" "$(cat $3)"
  fi
  exit 0
fi
