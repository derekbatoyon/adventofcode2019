#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "(3, 4)" > $TMPFILE
echo "8" >> $TMPFILE
python part1.py test1.txt | diff $TMPFILE -

echo "(5, 8)" > $TMPFILE
echo "33" >> $TMPFILE
python part1.py test2.txt | diff $TMPFILE -

echo "(1, 2)" > $TMPFILE
echo "35" >> $TMPFILE
python part1.py test3.txt | diff $TMPFILE -

echo "(6, 3)" > $TMPFILE
echo "41" >> $TMPFILE
python part1.py test4.txt | diff $TMPFILE -

echo "(11, 13)" > $TMPFILE
echo "210" >> $TMPFILE
python part1.py test5.txt | diff $TMPFILE -

echo "pass"
