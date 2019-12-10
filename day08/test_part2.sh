#!/bin/bash -e

TMPFILE=$(mktemp /tmp/XXXXXX.png)
trap "rm -f $TMPFILE" EXIT

python part2.py 2 2 test.txt $TMPFILE
cmp $TMPFILE test_result.png

echo "pass"
