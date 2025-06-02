import cv2

cap = cv2.VideoCapture()
print("Open camera...")
cap.open(0)

# To obtain the frame size, we first need to read one frame.
ret, frame = cap.read()
# The .shape property returns a tuple in the form (height, width, channels).
height, width, channels = frame.shape
print(f"frame: {height}x{width}x{channels}")
# Because the width is greater than the height, determine how much to trim in order to create a square frame.
padding = (width - height) // 2

for i in range(10000):
    ret, frame = cap.read()
    if ret is False:
        print("read failed.")
        break

    # Crop the frame to a square by removing padding from the left and right edges.
    # Padding: the extra width that will be removed from both the left and right edges of the frame.
    # [height_start:height_end, width_start:width_end, channel_start:channel_end]
    # A negative index (-padding) counts backward from the end of the width axis.
    crop_frame = frame[:, padding:-padding, :]
    mirror_frame = cv2.flip(crop_frame, 1)

    cv2.imshow("cam", mirror_frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
