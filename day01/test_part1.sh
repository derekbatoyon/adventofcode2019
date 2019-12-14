#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "2" > $TMPFILE
python part1.py test1.txt | diff $TMPFILE -

echo "2" > $TMPFILE
python part1.py test2.txt | diff $TMPFILE -

echo "654" > $TMPFILE
python part1.py test3.txt | diff $TMPFILE -

echo "33583" > $TMPFILE
python part1.py test4.txt | diff $TMPFILE -

echo "pass"
