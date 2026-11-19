#!/bin/bash
# Usage: ./loadtest.sh https://YOUR_PROJECT_ID.appspot.com
# Then watch: Console > App Engine > Instances (count rises 1 -> several)
for i in $(seq 1 300); do curl -s "$1/burn" -o /dev/null & done; wait
