from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from retinaface import RetinaFace
import cv2
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Function to detect faces using RetinaFace
def detect_faces(image):
    """
    Detects faces using RetinaFace and converts bounding boxes to JSON-compatible format.

    Args:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        list: List of bounding boxes for detected faces in the format:
              [{"box": [x, y, width, height]}].
    """
    faces = RetinaFace.detect_faces(image)
    face_boxes = []

    if isinstance(faces, dict):  # Check if any faces are detected
        for key in faces:
            facial_area = faces[key]["facial_area"]  # Get the bounding box
            x1, y1, x2, y2 = map(int, facial_area)  # Convert np.int64 to int
            face_boxes.append({"box": [x1, y1, x2 - x1, y2 - y1]})  # Convert to [x, y, width, height]

    return face_boxes


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        contents = await file.read()
        np_img = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if image is None:
            return JSONResponse(
                content={"error": "Unable to decode the image. Please upload a valid image."},
                status_code=400,
            )

        # Get original dimensions
        original_height, original_width = image.shape[:2]

        # Scale down the image if it's too large
        max_dimension = 800
        scale_factor = 1  # Default scale factor (no scaling)
        if max(original_height, original_width) > max_dimension:
            scale_factor = max_dimension / max(original_height, original_width)
            image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

        # Detect faces
        faces = detect_faces(image)

        # Scale bounding boxes back to the original resolution
        for face in faces:
            x, y, width, height = face["box"]
            face["box"] = [
                int(x / scale_factor),
                int(y / scale_factor),
                int(width / scale_factor),
                int(height / scale_factor),
            ]

            # Log the scaled bounding boxes
        print(f"Detected and scaled boxes (original resolution): {faces}")

        # Return detected faces and scaling information
        return JSONResponse(content={"faces": faces, "original_width": original_width, "original_height": original_height})
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content={"error": "Failed to process the image."}, status_code=500)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Zezwolenie na żądania ze wszystkich źródeł (na czas testów)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)