#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "2" > $TMPFILE
python part2.py test1.txt | diff $TMPFILE -

echo "2" > $TMPFILE
python part2.py test2.txt | diff $TMPFILE -

echo "966" > $TMPFILE
python part2.py test3.txt | diff $TMPFILE -

echo "50346" > $TMPFILE
python part2.py test4.txt | diff $TMPFILE -

echo "pass"
