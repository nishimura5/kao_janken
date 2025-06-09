import os

import cv2
import numpy as np

face_frame_path = os.path.join(os.path.dirname(__file__), "transparent.png")
blend_img = cv2.imdecode(np.fromfile(face_frame_path, np.uint8), cv2.IMREAD_UNCHANGED)

cap = cv2.VideoCapture()
print("Open camera...")
cap.open(0)

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

    show_img = frame.copy()

    # Get the dimensions of both the frame and the blend_img
    height, width, _ = frame.shape
    blend_height, blend_width, _ = blend_img.shape

    # Calculate the top, bottom, left, and right coordinates to center the blend_img on the frame
    top = (height - blend_height) // 2
    bottom = top + blend_height
    left = (width - blend_width) // 2
    right = left + blend_width

    # alpha_map: 4th(idx=3) channel of blend_img (alpha channel) normalized to [0, 1]
    alpha_map = blend_img[:, :, 3:] / 255.0
    show_img[top:bottom, left:right] = frame[top:bottom, left:right] * (1.0 - alpha_map) + blend_img[:, :, :3] * alpha_map

    put_str = f"count:{i}"
    cv2.putText(show_img, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 8)
    cv2.putText(show_img, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("cam", show_img)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        cv2.imwrite("photo.png", frame)
        print("Saved photo.")
        break
