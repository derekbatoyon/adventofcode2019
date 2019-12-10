#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo " *" > $TMPFILE
echo "* " >> $TMPFILE
python part2.py 2 2 test.txt | diff $TMPFILE -

echo "pass"
