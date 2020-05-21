#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "48226158" > $TMPFILE
python part1.py -1 test1.txt | diff $TMPFILE -

echo "34040438" > $TMPFILE
python part1.py -2 test1.txt | diff $TMPFILE -

echo "03415518" > $TMPFILE
python part1.py -3 test1.txt | diff $TMPFILE -

echo "01029498" > $TMPFILE
python part1.py -4 test1.txt | diff $TMPFILE -

echo "24176176" > $TMPFILE
python part1.py -100 test2.txt | diff $TMPFILE -

echo "73745418" > $TMPFILE
python part1.py -100 test3.txt | diff $TMPFILE -

echo "52432133" > $TMPFILE
python part1.py -100 test4.txt | diff $TMPFILE -

echo "pass"
