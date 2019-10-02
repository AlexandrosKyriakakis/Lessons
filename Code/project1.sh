#!/bin/sh
for i in {0..23}
do
    python3 project1.py <<EOF
$i
EOF
done
for i in {0..23}
do
    python3 project2.py <<EOF
$i
EOF
done
