#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "2772" > $TMPFILE
python part2.py test1.txt | diff $TMPFILE -

echo "4686774924" > $TMPFILE
python part2.py test2.txt | diff $TMPFILE -

echo "282270365571288" > $TMPFILE
python part2.py input.txt | diff $TMPFILE -

echo "pass"
