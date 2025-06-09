import os

import cv2
import numpy as np

import face_mesh


def overlay(src_img, blend_img):
    """
    Overlay a blend image with an alpha channel onto the center of the src_img.
    param src_img: The source image (BGR format).
    param blend_img: The blend image with an alpha channel (BGRA format).
    return: The resulting image with the blend image overlaid on the source image.
    """
    show_img = src_img.copy()

    height, width, _ = src_img.shape
    blend_height, blend_width, _ = blend_img.shape

    top = (height - blend_height) // 2
    bottom = top + blend_height
    left = (width - blend_width) // 2
    right = left + blend_width

    alpha_map = blend_img[:, :, 3:] / 255
    show_img[top:bottom, left:right] = src_img[top:bottom, left:right] * (1 - alpha_map) + blend_img[:, :, :3] * alpha_map

    return show_img


face_frame_path = os.path.join(os.path.dirname(__file__), "face_frame.png")
blend_img = cv2.imdecode(np.fromfile(face_frame_path, np.uint8), cv2.IMREAD_UNCHANGED)

cap = cv2.VideoCapture()
print("Open camera...")
cap.open(0)
# Set the camera resolution to 1920x1080
# If your camera does not support this resolution, try changing it to 1280x720 or another supported resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Create a FaceLandMarks detector object
detector = face_mesh.FaceLandMarks(maxFace=2)

ret, frame = cap.read()
height, width, channels = frame.shape
print(f"frame: {height}x{width}x{channels}")
padding = (width - height) // 2

for i in range(10000):
    ret, frame = cap.read()
    if ret is False:
        print("read failed.")
        break

    crop_frame = frame[:, padding:-padding, :]
    frame = cv2.flip(crop_frame, 1)

    # Face mesh detection and drawing
    detector.find_face_keypoints(frame)
    mesh_face_img = detector.draw(frame)

    show_img = overlay(mesh_face_img, blend_img)

    put_str = f"count:{i}"
    cv2.putText(show_img, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 8)
    cv2.putText(show_img, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("cam", show_img)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        cv2.imwrite("photo.png", frame)
        print("saved photo.")
        break
