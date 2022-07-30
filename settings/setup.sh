#!/usr/bin/env bash
echo $INPUT_GITHUB_LOGIN

if [[ $3 == "true" ]]; then
    git config --global url."https://$ACTIONS_ACCESS_USERNAME:$ACTIONS_ACCESS_KEY@github.com/".insteadOf "https://github.com/"
    echo "Github login is enabled"
else
    echo "Github login is disabled"
fi