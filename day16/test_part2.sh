#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "84462026" > $TMPFILE
python part2.py -100 test5.txt | diff $TMPFILE -

echo "78725270" > $TMPFILE
python part2.py -100 test6.txt | diff $TMPFILE -

echo "53553731" > $TMPFILE
python part2.py -100 test7.txt | diff $TMPFILE -

echo "pass"
