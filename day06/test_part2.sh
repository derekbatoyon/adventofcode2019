#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "4" > $TMPFILE
python part2.py < test2.txt | diff $TMPFILE -

echo "pass"
