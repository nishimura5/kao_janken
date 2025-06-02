import cv2

import face_mesh


cap = cv2.VideoCapture()
print("Open camera...")
cap.open(0)

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

    frame = frame[:, padding:-padding, :]
    frame = cv2.flip(frame, 1)

    # Face mesh detection and drawing
    detector.find_face_keypoints(frame)
    show_img = detector.draw(frame)

    cv2.imshow("cam", show_img)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        cv2.imwrite("photo.png", frame)
        print("saved photo.")
        break
