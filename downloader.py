import asyncio
import aiohttp
from PIL import UnidentifiedImageError
from filters import is_valid_face_with_glasses
from config import IMAGES_DIR, HEADERS
import os

async def load_and_filter(session, row, idx, global_idx, executor):
    url = row["image_url"]
    image_id = f"img_{global_idx + 1:06d}.jpg"

    try:
        #sending the http response to read and load the image
        async with session.get(url, headers=HEADERS) as response:
            if response.status != 200:
                return None
                
            # Skip SVG files (not a supported image format for face recognition)
            if "svg" in response.headers.get("Content-Type", ""):
                return None

            image_bytes = await response.read()
            loop = asyncio.get_running_loop()

            #Run the face-with-glasses check in a background thread
            result = await loop.run_in_executor(executor, is_valid_face_with_glasses, image_bytes)

            if result:
                #Save only valid images to disk
                result.save(os.path.join(IMAGES_DIR, image_id))
                return {"image_id": image_id, **row}
            return None

    except (aiohttp.ClientError, asyncio.TimeoutError, UnidentifiedImageError) as e:
        return None
    except Exception as e:
        return None
