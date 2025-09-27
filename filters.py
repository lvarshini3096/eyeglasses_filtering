import numpy as np
import cv2
from PIL import Image
from glasses_detector import GlassesClassifier
from yolo5face.get_model import get_model

def get_face_detector():
    if not hasattr(get_face_detector, "model"):
        get_face_detector.model = get_model("yolov5n", device=-1, min_face=100) 
        #setting face size min 100 pixels box
    return get_face_detector.model

def get_glasses_model():
    if not hasattr(get_glasses_model, "model"):
        get_glasses_model.model = GlassesClassifier(kind="eyeglasses", size="medium", device="cpu")
        #can use small/medium - didnt notice much time delay
    return get_glasses_model.model


def is_valid_face_with_glasses(image_bytes):
    """
    Function to load the models, detect the faces only that are more than 100 pixels, 
    cropping and resizing for Glass detector model
    Returns None if no face is found or no glasses are detected.
    """
    try:
        face_detector = get_face_detector()
        glasses_model = get_glasses_model()

        #Using image numpy array for both the models
        image_np_buffer = np.frombuffer(image_bytes, np.uint8)
        image_bgr = cv2.imdecode(image_np_buffer, cv2.IMREAD_COLOR)
        if image_bgr is None:
            return None

        boxes, _, _ = face_detector(image_bgr, target_size=512)
        if boxes is None or len(boxes) == 0:
            return None

        for box in boxes:
            x1, y1, x2, y2 = map(int, box)

            #Cropping the face to detect only worn glasses
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            face_crop = image_rgb[y1:y2, x1:x2]
            face_resized = cv2.resize(face_crop, (256, 256))
            
            if glasses_model.predict(face_resized) == "present":
                return Image.fromarray(image_rgb)
        return None
    except Exception as e:
        print(f"Error in is_valid_face_with_glasses: {e}")
        return None
