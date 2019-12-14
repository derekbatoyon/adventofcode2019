#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "42" > $TMPFILE
python part1.py test1.txt | diff $TMPFILE -

echo "pass"
