#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "[3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]" > $TMPFILE
python part1.py test1.txt | diff $TMPFILE -

echo "[2, 0, 0, 0, 99]" > $TMPFILE
python part1.py test2.txt | diff $TMPFILE -

echo "[2, 3, 0, 6, 99]" > $TMPFILE
python part1.py test3.txt | diff $TMPFILE -

echo "[2, 4, 4, 5, 99, 9801]" > $TMPFILE
python part1.py test4.txt | diff $TMPFILE -

echo "[30, 1, 1, 4, 2, 5, 6, 0, 99]" > $TMPFILE
python part1.py test5.txt | diff $TMPFILE -

echo "pass"
