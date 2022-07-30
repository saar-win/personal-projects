#!/usr/bin/env bash
echo $INPUT_GITHUB_LOGIN
echo $INPUT_ACTIONS_ACCESS_USERNAME
echo $INPUT_ACTIONS_ACCESS_KEY

if [[ $INPUT_GITHUB_LOGIN == "true" ]]; then
    git config --global url."https://$INPUT_ACTIONS_ACCESS_USERNAME:$INPUT_ACTIONS_ACCESS_KEY@github.com/".insteadOf "https://github.com/"
    echo "Github login is enabled"
else
    echo "Github login is disabled"
fi