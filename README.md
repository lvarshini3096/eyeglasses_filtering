# Eyesight Glasses Filtering - Data processing and filtering system

## About

This project processes dataset parquets/shards sequentially, applies image filters or classification as per the criteria, and saves the filtered output images.

Specifically, the criteria include:

- Detecting faces using a face recognition model such as YoloV5Face.
- Checking if the detected face is larger than 100x100 pixels.
- Using the [glasses_detector](https://github.com/mantasu/glasses-detector) model to determine if the person is wearing eyesight glasses.

Filtered images and metadata are saved for further use.

## Project Structure

```
├── main.py # main script to link dataset to be fetched and starting the process
├── processor.py # Processing each shard and setting up async task for each row
├── filters.py # Filtering/classification logic
├── downloader.py #running session to make http requests for image loading
├── config.py # Configuration and constants
├── requirements.txt # Required Python dependencies
├── README.md 
└── filtered_data/ # Folder where filtered_images/ filtered_metadata are saved
```
---

## Getting Started

Follow these instructions to set up and run the project.

### Prerequisites

- Python 3.8 or higher
- Internet connection to download parquet/shards from huggingface and dependencies

---

### 1. Clone the Repository

```
git clone https://github.com/lvarshini/eyeglasses_filtering.git
cd eyeglasses_filtering
```

### 2. Create and Activate a Virtual Environment (Recommended)

macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```
Windows:
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Run the Processing Script
```
python main.py
```
The script will process each data shard sequentially. Filtered images and metadata will be saved inside the filtered_data/ folder.
