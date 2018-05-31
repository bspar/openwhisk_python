#!/bin/bash

if [ $# -ne 1 ]; then
    echo "[-] no filename supplied"
    exit -1
fi;
if [ ! -f "$1" ]; then
    echo "[-] file not found"
    exit -1
fi;
if [ ! -f "requirements.txt" ]; then
    echo "[-] requirements.txt not found"
    exit -1
fi;

docker run --rm -v "$PWD:/tmp" bspar/openwhisk-runtime-python:python3-latest bash \
  -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"

cp $1 __main__.py
filename=$(basename -- "$1")
name="${filename%.*}"
zip -r "$name.zip" virtualenv __main__.py

rm __main__.py
rm -rf virtualenv

echo "[+] All done"
echo "[+] Created $name.zip"
