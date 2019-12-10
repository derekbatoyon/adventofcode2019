#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

tr , '\n' < test1.txt > $TMPFILE
python part1.py test1.txt | diff $TMPFILE -

echo "16" > $TMPFILE
python part1.py test2.txt | tr -d '\n' | wc -c | diff --ignore-all-space $TMPFILE -

echo "1125899906842624" > $TMPFILE
python part1.py test3.txt | diff $TMPFILE -

echo "pass"
