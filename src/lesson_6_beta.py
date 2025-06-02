import os

import cv2
import numpy as np

# Make the path to the face frame image
# __file__ is the path to the current file (lesson_6_beta.py) 
face_frame_path = os.path.join(os.path.dirname(__file__), "face_frame.png")
print(f"face_frame_path: {face_frame_path}")

# To read the non-ASCII file path correctly, we use cv2.imdecode with np.fromfile
# If you ASCII file path, you can use cv2.imread() directly
# cv2.IMREAD_UNCHANGED flag is used to read the image with alpha channel (transparency)
png_img = cv2.imdecode(np.fromfile(face_frame_path, np.uint8), cv2.IMREAD_UNCHANGED)
height, width, channels = png_img.shape
print(f"png_img: {height}x{width}x{channels}")

cv2.imshow("png_RGB", png_img[:, :, :3])
# Display the alpha channel of the PNG image
# The black area in the alpha channel represents the transparent area
cv2.imshow("png_alpha", png_img[:, :, 3])
# Wait for a key press indefinitely
key = cv2.waitKey(0)
if key == ord("q"):
    cv2.destroyAllWindows()
