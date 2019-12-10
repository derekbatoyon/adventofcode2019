#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "139629729" > $TMPFILE
python part2.py test4.txt 9,8,7,6,5 | diff $TMPFILE -
python part2.py test4.txt | diff $TMPFILE -

echo "18216" > $TMPFILE
python part2.py test5.txt 9,7,8,5,6 | diff $TMPFILE -
python part2.py test5.txt | diff $TMPFILE -

echo "pass"
