#!/usr/bin/env bash

echo $3

if [[ $3 == "true" ]]; then
    echo "Github login is enabled"
    git config --global url."https://$ACTIONS_ACCESS_USERNAME:$ACTIONS_ACCESS_KEY@github.com/".insteadOf "https://github.com/"
else
    echo "Github login is disabled"
fi