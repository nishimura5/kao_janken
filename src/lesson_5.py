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

    crop_frame = frame[:, padding:-padding, :]
    frame = cv2.flip(crop_frame, 1)

    # Create a copy of the frame to draw on
    show_img = frame.copy()

    put_str = f"count:{i}"
    cv2.putText(show_img, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 8)
    cv2.putText(show_img, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("cam", show_img)

    key = cv2.waitKey(1)
    # If 'q' key is pressed, break the loop
    if key == ord("q"):
        break
    # If 's' key is pressed, save the current frame as a photo.png and break the loop
    elif key == ord("s"):
        cv2.imwrite("photo.png", frame)
        print("Saved photo.")
        break
