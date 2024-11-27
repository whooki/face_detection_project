from mtcnn import MTCNN
import cv2

def detect_faces(image):
    """
    Wykrywa twarze na obrazie za pomocą MTCNN.

    Args:
        image (numpy.ndarray): Obraz w formacie BGR (np. odczytany za pomocą OpenCV).

    Returns:
        list: Lista słowników, gdzie każdy słownik zawiera współrzędne prostokąta twarzy w formacie:
              {"box": [x, y, width, height]}
    """
    # Tworzenie instancji MTCNN
    detector = MTCNN()

    # Detekcja twarzy
    results = detector.detect_faces(image)

    # Konwersja wyników na odpowiedni format
    faces = []
    for result in results:
        box = result["box"]  # Współrzędne prostokąta: [x, y, width, height]
        faces.append({"box": box})

    return faces
