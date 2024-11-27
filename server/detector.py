from mtcnn import MTCNN
import cv2
import numpy as np

def detect_faces(image):
    """
    Detects faces in an image and handles sideways or rotated images.

    Args:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        list: List of detected faces with bounding boxes.
    """
    detector = MTCNN()
    faces = []

    # Try detecting faces in the original orientation
    results = detector.detect_faces(image)
    if results:
        return [{"box": result["box"]} for result in results]

    # If no faces detected, rotate and retry
    for angle in [90, 180, 270]:
        rotated_image = rotate_image(image, angle)
        results = detector.detect_faces(rotated_image)
        if results:
            # Adjust coordinates back to original image orientation
            for result in results:
                box = adjust_box_coordinates(result["box"], image, angle)
                faces.append({"box": box})
            break  # Stop if faces are found

    return faces

def rotate_image(image, angle):
    """
    Rotates an image by a specified angle.

    Args:
        image (numpy.ndarray): Input image.
        angle (int): Angle to rotate (90, 180, or 270 degrees).

    Returns:
        numpy.ndarray: Rotated image.
    """
    if angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image

def adjust_box_coordinates(box, image, angle):
    """
    Adjust bounding box coordinates after image rotation.

    Args:
        box (list): Original bounding box [x, y, width, height].
        image (numpy.ndarray): Original image.
        angle (int): Rotation angle (90, 180, or 270 degrees).

    Returns:
        list: Adjusted bounding box [x, y, width, height].
    """
    x, y, width, height = box
    h, w = image.shape[:2]  # Original dimensions of the image

    if angle == 90:
        return [h - y - height, x, height, width]
    elif angle == 180:
        return [w - x - width, h - y - height, width, height]
    elif angle == 270:
        return [y, w - x - width, height, width]
    return box
