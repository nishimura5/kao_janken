import cv2

cap = cv2.VideoCapture()
print("Open camera...")
cap.open(0)

for i in range(10000):
    ret, frame = cap.read()
    if ret is False:
        print("read failed.")
        break

    # Crop the frame to a square (400x400) section
    # [height_start:height_end, width_start:width_end, channel_start:channel_end]
    # left-top is origin (0, 0)
    crop_frame = frame[100:500, 150:550, :]

    mirror_frame = cv2.flip(crop_frame, 1)

    cv2.imshow("cam", mirror_frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
