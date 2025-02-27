#!/bin/bash -e

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

python part2.py test6.txt > $TMPFILE 2> /dev/null
diff $TMPFILE - <<OUTPUT
1 (8, 1)
2 (9, 0)
3 (9, 1)
4 (10, 0)
5 (9, 2)
6 (11, 1)
7 (12, 1)
8 (11, 2)
9 (15, 1)
10 (12, 2)
11 (13, 2)
12 (14, 2)
13 (15, 2)
14 (12, 3)
15 (16, 4)
16 (15, 4)
17 (10, 4)
18 (4, 4)
19 (2, 4)
20 (2, 3)
21 (0, 2)
22 (1, 2)
23 (0, 1)
24 (1, 1)
25 (5, 2)
26 (1, 0)
27 (5, 1)
28 (6, 1)
29 (6, 0)
30 (7, 0)
31 (8, 0)
32 (10, 1)
33 (14, 0)
34 (16, 1)
35 (13, 3)
36 (14, 3)
OUTPUT

python part2.py test5.txt 11,13 > $TMPFILE 2> /dev/null

grep '^1 '   $TMPFILE | grep --quiet '(11, 12)$'
grep '^2 '   $TMPFILE | grep --quiet '(12, 1)$'
grep '^3 '   $TMPFILE | grep --quiet '(12, 2)$'
grep '^10 '  $TMPFILE | grep --quiet '(12, 8)$'
grep '^20 '  $TMPFILE | grep --quiet '(16, 0)$'
grep '^50 '  $TMPFILE | grep --quiet '(16, 9)$'
grep '^100 ' $TMPFILE | grep --quiet '(10, 16)$'
grep '^199 ' $TMPFILE | grep --quiet '(9, 6)$'
grep '^200 ' $TMPFILE | grep --quiet '(8, 2)$'
grep '^201 ' $TMPFILE | grep --quiet '(10, 9)$'
grep '^300 ' $TMPFILE | grep --quiet '(11, 1)$'

echo "pass"
