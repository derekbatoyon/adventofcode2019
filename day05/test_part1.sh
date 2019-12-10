#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "5" > $TMPFILE
python part1.py echo.txt < $TMPFILE | diff $TMPFILE -

# these test pass if execution ends without incident
python part1.py test1.txt
python part1.py test2.txt

echo "pass"
