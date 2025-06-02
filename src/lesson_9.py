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

    frame = frame[:, padding:-padding, :]
    frame = cv2.flip(frame, 1)

    detector.find_face_keypoints(frame)
    mesh_face_img = detector.draw(frame)

    show_img = overlay(mesh_face_img, blend_img)

    mouths = detector.get_mouth_xy()
    if len(mouths) > 0:
        mouth = mouths[0]
        # Calculate the distance between landmarks 0 and 17 (vertical) and 78 and 308 (horizontal)
        # and determine the gesture based on the ratio of these distances
        # 0: mouth left corner, 17: mouth right corner, 78: mouth upper lip, 308: mouth lower lip
        distance_0_17 = ((mouth[0][0] - mouth[17][0]) ** 2 + (mouth[0][1] - mouth[17][1]) ** 2) ** 0.5
        distance_78_308 = ((mouth[78][0] - mouth[308][0]) ** 2 + (mouth[78][1] - mouth[308][1]) ** 2) ** 0.5
        ratio = distance_0_17 / distance_78_308
        if ratio < 0.5:
            janken = "gu"
        elif ratio > 1.5:
            janken = "choki"
        elif distance_0_17 > 100 and distance_78_308 > 200:
            janken = "pa"
        else:
            janken = "unknown"
        put_str = f"distance vertical:{distance_0_17:5.1f}, horizontal:{distance_78_308:5.1f}, ratio:{ratio:4.2f} ({janken})"
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
