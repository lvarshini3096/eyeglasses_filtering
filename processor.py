import aiohttp
from concurrent.futures import ProcessPoolExecutor
from tqdm.asyncio import tqdm_asyncio
from downloader import load_and_filter

#start_idx is the starting idx for that particular shard and idx if the relative idx for that image
#Processes all rows in the given dataframe to download and filter images
async def process_all(df, start_idx):
    connector = aiohttp.TCPConnector(limit=50)
    executor = ProcessPoolExecutor()

    #Open a single HTTP session for all image downloads
    async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=None)) as session:

        # Prepare a list of async tasks for each image row in the dataframe
        tasks = []
        for idx, row in df.iterrows():
            task = load_and_filter(session, row, idx, start_idx + idx, executor)
            tasks.append(task)

        #Set the Progress bar to view the task running
        results = await tqdm_asyncio.gather(*tasks)
    return [r for r in results if r]
