import os

#Output file directories
OUTPUT_DIR = "filtered_data"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "filtered_images")
CSV_PATH = os.path.join(OUTPUT_DIR, "filtered_metadata.csv")
HEADERS = {"User-Agent": "Mozilla/5.0 (LekhaBot/1.0)"}

os.makedirs(IMAGES_DIR, exist_ok=True)
