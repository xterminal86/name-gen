#!/bin/bash

if [ $# -ne 1 ]; then
  echo "${0} <NAMES.txt>"
  exit 1
fi

arg=$1

ar=$(cat "${arg}" | sort)

for name in ${ar[@]}; do
  python3 tokenizer.py "${name}"
done
