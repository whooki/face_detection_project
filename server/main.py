from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from detector import detect_faces
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from mtcnn import MTCNN

app = FastAPI()

# Funkcja wykrywająca twarze
def detect_faces(image):
    detector = MTCNN()
    results = detector.detect_faces(image)
    faces = [{"box": result["box"]} for result in results]
    return faces

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Odczytanie zawartości przesłanego pliku
        contents = await file.read()
        np_img = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Sprawdzenie poprawności obrazu
        if image is None:
            return JSONResponse(
                content={"error": "Nie udało się zdekodować obrazu. Upewnij się, że plik jest prawidłowym obrazem."},
                status_code=400,
            )

        # Detekcja twarzy
        faces = detect_faces(image)

        # Obsługa przypadku, gdy nie wykryto żadnych twarzy
        if not faces:
            return JSONResponse(content={"faces": [], "message": "Nie wykryto żadnych twarzy na obrazie."})


        # Zwrot wyników w formacie JSON
        return JSONResponse(content={"faces": faces})
    except Exception as e:
        print(f"Błąd: {e}")
        return JSONResponse(content={"error": "Nie udało się przetworzyć obrazu."}, status_code=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Zezwolenie na żądania ze wszystkich źródeł (na czas testów)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
