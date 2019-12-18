#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "31" > $TMPFILE
python part1.py test1.txt | diff $TMPFILE -

echo "165" > $TMPFILE
python part1.py test2.txt | diff $TMPFILE -

echo "13312" > $TMPFILE
python part1.py test3.txt | diff $TMPFILE -

echo "180697" > $TMPFILE
python part1.py test4.txt | diff $TMPFILE -

echo "2210736" > $TMPFILE
python part1.py test5.txt | diff $TMPFILE -

echo "pass"
