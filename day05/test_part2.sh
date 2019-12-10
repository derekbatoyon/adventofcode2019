#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

echo "5" > $TMPFILE
python part2.py echo.txt < $TMPFILE | diff $TMPFILE -

# these test pass if execution ends without incident
python part2.py test1.txt
python part2.py test2.txt

# equal to 8? (using position mode)
echo "0" > $TMPFILE
echo "7" | python part2.py compare_test1.txt | diff $TMPFILE -
echo "1" > $TMPFILE
echo "8" | python part2.py compare_test1.txt | diff $TMPFILE -
echo "0" > $TMPFILE
echo "9" | python part2.py compare_test1.txt | diff $TMPFILE -

# less than 8? (using position mode)
echo "1" > $TMPFILE
echo "7" | python part2.py compare_test2.txt | diff $TMPFILE -
echo "0" > $TMPFILE
echo "8" | python part2.py compare_test2.txt | diff $TMPFILE -
echo "9" | python part2.py compare_test2.txt | diff $TMPFILE -

# equal to 8? (using immediate mode)
echo "0" > $TMPFILE
echo "7" | python part2.py compare_test3.txt | diff $TMPFILE -
echo "1" > $TMPFILE
echo "8" | python part2.py compare_test3.txt | diff $TMPFILE -
echo "0" > $TMPFILE
echo "9" | python part2.py compare_test3.txt | diff $TMPFILE -

# less than 8? (using immediate mode)
echo "1" > $TMPFILE
echo "7" | python part2.py compare_test4.txt | diff $TMPFILE -
echo "0" > $TMPFILE
echo "8" | python part2.py compare_test4.txt | diff $TMPFILE -
echo "9" | python part2.py compare_test4.txt | diff $TMPFILE -

# input non-zero? (using position mode)
echo "1" > $TMPFILE
echo "-1" | python part2.py jump_test1.txt | diff $TMPFILE -
echo "0" > $TMPFILE
echo "0" | python part2.py jump_test1.txt | diff $TMPFILE -
echo "1" > $TMPFILE
echo "1" | python part2.py jump_test1.txt | diff $TMPFILE -

# input non-zero? (using immediate mode)
echo "1" > $TMPFILE
echo "-1" | python part2.py jump_test2.txt | diff $TMPFILE -
echo "0" > $TMPFILE
echo "0" | python part2.py jump_test2.txt | diff $TMPFILE -
echo "1" > $TMPFILE
echo "1" | python part2.py jump_test2.txt | diff $TMPFILE -

# larger example
echo "999" > $TMPFILE
echo "7" | python part2.py larger_example.txt | diff $TMPFILE -
echo "1000" > $TMPFILE
echo "8" | python part2.py larger_example.txt | diff $TMPFILE -
echo "1001" > $TMPFILE
echo "9" | python part2.py larger_example.txt | diff $TMPFILE -

echo "pass"
