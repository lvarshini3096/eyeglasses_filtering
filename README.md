# Eyesight Glasses Filtering - Data Processing and Filtering System

This project implements an efficient and reliable pipeline to process a **large-scale image dataset**, detecting and filtering images containing faces wearing **eyesight glasses**. It leverages **asynchronous downloading** and **parallel machine learning-based filtering** to efficiently extract filtered images and their metadata for research and easy searching.

---

## 🎯 Objective

The core aim is to build a high-throughput system that can process massive image datasets, filtering for a specific visual characteristic (faces with eyesight glasses). The pipeline extracts the relevant images and their metadata, saving them for researchers to easily search and utilize.

| Resource | Link |
| :--- | :--- |
| **HuggingFace Dataset (Output)** | `https://huggingface.co/datasets/lvarshini3096/filtered_glasses_dataset` |

---

## 💻 System Design and Technology Choices

The system is designed for high-throughput data processing, combining efficient networking with parallel computing for the best performance.

### High-Performance Pipeline

* **Data Handling**: The system processes large-scale image dataset shards (parquet files) sequentially to maintain data consistency and prevent memory overload. The dataset source can be easily updated in `main.py`.
* **Async Image Downloading**: Utilizes Python's `asyncio` and `aiohttp` to perform **concurrent downloads**. This allows the system to fetch multiple images simultaneously, avoiding the bottleneck of waiting for sequential network requests.
* **Parallel Image Filtering**: **CPU-intensive filtering tasks** (face and glasses detection) are executed in parallel using a **pool of worker processes**. This prevents blocking of the main program flow, ensuring full utilization of available CPU cores.

### Filtering Logic and Models

The filtering process uses a two-stage approach with specialized Machine Learning models:

| Component | Model | Details & Rationale |
| :--- | :--- | :--- |
| **Face Detection** | **YOLOv5Face** | Chosen for its **lightweight, speed, and accuracy** compared to other models like MTCNN. Faces smaller than **$100 \times 100$ pixels** are ignored to ensure image quality. |
| **Glasses Detection** | **GlassesClassifier** (Link: `glasses-detector` repository) | Selected because it was specifically trained for **eyesight glasses** (not sunglasses) and is **open source**. Faces are cropped based on the YOLOv5Face box and resized to **$256 \times 256$ pixels** before classification. |

### Robustness and Output

* **Error Handling**: The system is resilient, designed to **skip corrupted images**, invalid formats, and network failures without crashing.
* **Progress and IDs**: Progress bars are shown during processing. It maintains consistent, **unique global IDs** across shards to prevent filename collisions.
* **Output**: Filtered images are saved locally in the `filtered_data/images` directory. The metadata for filtered images is saved to `filtered_data/metadata.csv` with the new `global_id` for easy referencing. The filter criteria can be easily updated or changed in `filters.py`.

---

## 🚀 Scaling and Future Enhancements

Currently, the system processes one shard at a time, taking about **23 minutes per shard**. To scale for processing billions of images, the architecture can be upgraded:

1.  **Parallel Shard Processing**: Depending on the capacity of the processing unit, the system can be upgraded to process multiple shards in parallel to significantly increase throughput.
2.  **Cloud-Native Scaling**: Utilizing AWS services would make parallel processing faster and more manageable:
    * **Amazon S3**: For scalable storage of images and metadata, concurrently accessible by multiple processing units.
    * **Amazon EC2**: To run distributed data processing workloads, where multiple servers handle different shards in parallel.
    * **AWS Lambda**: For running lightweight functions like image filtering or metadata updates, automatically scaling based on workload.

---

## Project Structure

The code is structured to be modular, making it easy to edit the dataset source or update filter criteria.

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
