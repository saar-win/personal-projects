#!/usr/bin/env bash

if [[ $GITHUB_LOGIN == "true" ]]; then
    echo "Github login is enabled"
    git config --global url."https://$ACTIONS_ACCESS_USERNAME:$ACTIONS_ACCESS_KEY@github.com/".insteadOf "https://github.com/"
fi