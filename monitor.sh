#!/bin/bash
until python ethcrash_scrape.py; do
    echo "'ethcrash_scrape.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
