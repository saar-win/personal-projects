#!/bin/bash
obj=$(cat $1 | jq)

echo "::set-output name=result::$obj"