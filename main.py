import os
import asyncio
from datasets import load_dataset
from config import OUTPUT_DIR, CSV_PATH
from processor import process_all
import pandas as pd
import multiprocessing

def main():
    
    # Download the first two data shards from the Wikimedia WIT dataset on HuggingFace
    base_url = "https://huggingface.co/datasets/wikimedia/wit_base/resolve/main/data"
    total_shards = 2  #Update to include as many shards as required
    
    shard_urls = []
    for i in range(total_shards):
        shard_name = f"train-{i:05d}-of-00330.parquet"
        shard_urls.append(f"{base_url}/{shard_name}")

    # Ensure output directory exists and remove previous CSV if it exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)

    #set a global indexes for multiple shards to avoid idx overlap
    global_idx = 0

    #Iterate through each shard and convert them into pandas dataframe
    for shard_num, shard_url in enumerate(shard_urls):
        print(f"____Processing Shard {shard_num + 1}/{len(shard_urls)}____")
        dataset = load_dataset("parquet", data_files={"train": shard_url}, split="train")
        df = dataset.to_pandas()
        print(f"Loaded {len(df)} records from shard")

        #Run asynchronous processing pipeline to detect valid images
        filtered = asyncio.run(process_all(df, global_idx))

        #Save the metadata of filtered images to a new csv file
        if filtered:
            pd.DataFrame(filtered).to_csv(CSV_PATH, index=False, mode='a', header=not os.path.exists(CSV_PATH))
            print(f"Saved {len(filtered)} filtered images from this shard")
        else:
            print("No valid images found in this shard.")

        global_idx += len(df)

if __name__ == "__main__":
    
    try:
        #multiprocessor set to spawn start instead of default forked start
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        pass

    main()
