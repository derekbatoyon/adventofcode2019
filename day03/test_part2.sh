#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "30.0" > $TMPFILE
python part2.py test1.txt | diff $TMPFILE -

echo "610.0" > $TMPFILE
python part2.py test2.txt | diff $TMPFILE -

echo "410.0" > $TMPFILE
python part2.py test3.txt | diff $TMPFILE -

echo "pass"
