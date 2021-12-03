#!/bin/bash

START=`date +%s`
while [ $(( $(date +%s) - 600 )) -lt $START ]; do
    echo "Checking"
    x="lsof -i -P -n | grep LISTEN | grep 8080"
    eval $x
    sleep 3
done