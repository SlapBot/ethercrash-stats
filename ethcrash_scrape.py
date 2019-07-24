import requests
from bs4 import BeautifulSoup as BS
from aiohttp import ClientSession
import asyncio
import subprocess
import os
import csv
import time

start = 2
end = 632120

batch_size = 5

store_filename = "async_ethcrash_stats.csv"

GET_URL = "https://www.ethcrash.io/game/{0}"

 
# A simple async fetch function
async def fetch(url, session):
    # (a)waiting for for the server response to come back (during that time the event loop is free)
    async with session.get(url) as response:
        # reading the response and parsing in is also async operation
        print("Url processed: {0}".format(url))
        return await response.text()
 
 
# The main function to download, get the number of posts to download as n
async def run(indexes):
    # fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        # init the future, each future is a url-request
        tasks = [asyncio.ensure_future(fetch(GET_URL.format(i)
                                             , session)) for i in indexes]
        # wait for all responses to come back
        return await asyncio.gather(*tasks)
 

# takes the indexes as list of indexes to go through
def get_next_indexes_results(indexes):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(indexes))
    return loop.run_until_complete(future)


def update_start(start, filename):
	if (os.path.exists(filename)):
		last_line = subprocess.check_output(['tail', '-1', filename])
		game_number = last_line.decode().split(",")[0]
		return int(game_number) + 1
	return start

def get_url(game_number):
	url = "https://www.ethcrash.io/game/{0}"
	return url.format(game_number)

def make_request(url):
	r = requests.get(url)
	if r.ok:
		print("Successfully requested url: {0}".format(url))
		return r.text
	print("Failed to request url: {0}".format(url))
	return False

def parse_request(html):
	soup = BS(html, 'html.parser')
	try:
		game_number = soup.find("h1", class_="panel-title").text.encode('ascii', 'replace').decode().split("?")[1]
		date = soup.find("div", class_="panel-body").find_all("p")[1].text.encode("ascii", 'replace').decode().split("on ")[-1]
		crash = soup.find("div", class_="panel-body").find("p").text.encode("ascii", 'replace').decode().split("?")[1]
	except Exception as e:
		print(e)
		print(html)
		exit()
	return (game_number, date, crash)

def write_to_csv(filename, data):
	with open(filename, 'a') as csv_file:
		file_writer = csv.writer(csv_file)
		for row in data:
			file_writer.writerow(row)
	return True


def batches(iterable, n = 1):
    current_batch = []
    for item in iterable:
        current_batch.append(item)
        if len(current_batch) == n:
            yield current_batch
            current_batch = []
    if current_batch:
        yield current_batch

def main():
	now = time.time()
	updated_start = update_start(start, store_filename)
	for batch in batches(range(updated_start, end+1), batch_size):
		start_game = time.time()
		data = []
		html_data = get_next_indexes_results(batch)
		print("All Urls processed")
		for html in html_data:
			row = parse_request(html)
			data.append(row)
		data.sort(key=lambda x: x[1])
		end_game = time.time()
		print("Elapsed time for game numbers from {0} to {1} is: {2}".format(batch[0], batch[-1], end_game-start_game))
		write_to_csv(store_filename, data)
		done = time.time()
		time.sleep(3)
	print("Elapsed time: {0}".format(done-now))
	print("Average Elapsed time: {0}".format((done-now)/(end+1-updated_start)))


if __name__ == '__main__':
	main()
