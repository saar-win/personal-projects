#!/bin/bash

sudo chown -R runner .
git config --global user.email "saar1122@gmail.com"
git config --global user.name "saar-win"
git checkout -b "test_123"
git add -A
git commit -am "hey"
git push --set-upstream origin test_123