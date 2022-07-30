#!/bin/sh -l


echo "key_1 $1"
echo "key_2 $2"
echo "key_3 $3"
echo "key_4 $4"
time=$(date)
echo "::set-output name=time::$time"