#!/bin/bash

# base64 encode the file.
#split the file into 4864 chunks.
#split -b 4864 ./un.rpyc-base64 unrpycbase64
#output it as varname#=file content

  if [[ ! -f $1 ]]
  then
  echo -e "$0 <file to base64> <var name> <bits to split [optional]>\n"
  exit 1
  fi


b64fn=$1.base64
bits=4864
  if test $3
  then
  bits=$3
  fi

base64 -w0 $1 > $b64fn

split -b $bits $b64fn ${b64fn}-

i=1
  for fn in `ls ${b64fn}-*`
  do
  echo -n "set $2$i="
  cat $fn
  echo -e "\n"
  i=$(( i + 1 ))
  done

exit 0
