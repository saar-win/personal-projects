#!/bin/sh
set -e

crond -b

flask run --host="0.0.0.0"
