#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "43210" > $TMPFILE
python part1.py test1.txt 4,3,2,1,0 | diff $TMPFILE -
python part1.py test1.txt | diff $TMPFILE -

echo "54321" > $TMPFILE
python part1.py test2.txt 0,1,2,3,4 | diff $TMPFILE -
python part1.py test2.txt | diff $TMPFILE -

echo "65210" > $TMPFILE
python part1.py test3.txt 1,0,4,3,2 | diff $TMPFILE -
python part1.py test3.txt | diff $TMPFILE -

echo "pass"
