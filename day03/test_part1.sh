#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "6.0" > $TMPFILE
python part1.py < test1.txt | tail -n 1 | diff $TMPFILE -

echo "159.0" > $TMPFILE
python part1.py < test2.txt | tail -n 1 | diff $TMPFILE -

echo "135.0" > $TMPFILE
python part1.py < test3.txt | tail -n 1 | diff $TMPFILE -

echo "pass"
