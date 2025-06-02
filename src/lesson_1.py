import cv2

# Create a VideoCapture object
cap = cv2.VideoCapture()
# Display a message indicating that the camera is being opened
print("Open camera...")
# Open the first camera (usually the built-in webcam, indexed as 0)
cap.open(0)

for i in range(10000):
    # Read a frame from the camera
    # frame: a Numpy array representing the image captured by the camera
    # ret: a boolean indicating if the frame was read successfully
    ret, frame = cap.read()

    # If reading the frame failed, print an error message and break the loop
    if ret is False:
        print("read failed.")
        break

    # Mirror (flip) the frame horizontally
    mirror_frame = cv2.flip(frame, 1)

    # Display the frame in a window titled 'cam'
    cv2.imshow("cam", mirror_frame)

    # Wait for 1 millisecond and get the key pressed
    # key: an integer representing the key pressed
    # If no key is pressed, key will be -1
    # If a key is pressed, it will return the ASCII value of the key
    key = cv2.waitKey(1)
    # If 'q' key is pressed, break the loop
    if key == ord("q"):
        break
