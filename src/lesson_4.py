import cv2

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

    # frame variable is updated with the cropped and mirrored frame
    crop_frame = frame[:, padding:-padding, :]
    frame = cv2.flip(crop_frame, 1)

    # Put counter
    put_str = f"count:{i}"
    cv2.putText(frame, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 8)
    cv2.putText(frame, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("cam", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
