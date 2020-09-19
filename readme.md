# Ethercrash (Previously Ethcrash) Scraper

A simple asynchronous script to scrape all of the games of [ethercrash](https://www.ethercrash.io/) from any given interval, like game number 100 to 12000, etc
with fail checks to restart the script from where it left in any case of error.

![](https://github.com/SlapBot/ethercrash-stats/blob/master/screenshot.PNG)

## Data

Data is stored in `ethcrash_stats.csv`, fields that are scraped are as follows:

1. Game Number
2. Date
3. Crash value

## Installation

### Pre-requisites

1. Python3
2. pip
3. virtualenv

### Instructions

1. Clone the repo: `git clone https://github.com/slapbot/ethercrash-stats`
2. Cd into the directory: `cd ethercrash-stats-scraper`
3. Create a virtualenv: `python3 -m venv ethercrash-stats-scraper-env`
4. Activate the env: `source ethercrash-stats-scraper-env/bin/activate`
5. Install the application dependencies: `pip install -r requirements.txt`

## Usage

1. Open up the `ethcrash_scrape.py` file and put the values at `start`, `end` variables that defines the starting and ending game_numbers to scrape the data between. (Like start = 100, ending = 10000) meaning scrape from game_number 100 to 10000
2. Run `ethcrash_scrape.py`
3. Can also run the shell script as well: `./monitor.sh` - but ensure that you activate your virtualenv.


## Why?

I don't know - was just clearing my system and found this program that I wrote for someone - Figured to host it in github.

With the dataset in hand, you can deploy various strategies to forecast the crash values to bet on the platform.

