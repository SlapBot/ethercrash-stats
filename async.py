import asyncio
 
from aiohttp import ClientSession
 
GET_URL = "https://www.ethcrash.io/game/{0}"

 
# A simple async fetch function
async def fetch(url, session):
    # (a)waiting for for the server response to come back (during that time the event loop is free)
    async with session.get(url) as response:
        # reading the response and parsing in is also async operation
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
 
 
def get_last_n_stories(indexes):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(indexes))
    return loop.run_until_complete(future)

 
responses = get_last_n_stories([i for i in range(2, 10)])
print(responses)
