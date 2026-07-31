import os
import random

import cv2
import numpy as np

import face_mesh


def main():
    gesture_images = load_gesture_images()

    cap = cv2.VideoCapture()
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
    additional_padding = 100
    gesture_image_size = max(40, int(min(height // 4, 240) * 0.7))
    gesture_images = {gesture: cv2.resize(image, (gesture_image_size, gesture_image_size)) for gesture, image in gesture_images.items()}

    # Initialize NPC's HP, random gesture, and round counter
    # NPC: Non-Player Character
    npc_hp = 100
    npc_jan = random.choice(["gu", "choki", "pa"])
    janken_count = 0

    for i in range(10000):
        ret, frame = cap.read()
        if ret is False:
            print("read failed.")
            break

        crop_frame = frame[additional_padding:-additional_padding, padding + additional_padding : -padding - additional_padding, :]
        frame = cv2.flip(crop_frame, 1)

        detector.find_face_keypoints(frame)
        black_img = np.zeros_like(frame)
        mesh_black_img = detector.draw(black_img)
        mesh_face_img = detector.draw(frame)

        show_img = frame.copy()

        # Concatenate the frame and the blend_img
        small_face_img = cv2.resize(mesh_face_img, None, fx=0.5, fy=0.5)
        small_black_img = cv2.resize(mesh_black_img, None, fx=0.5, fy=0.5)
        frame_mesh_img = cv2.vconcat([small_face_img, small_black_img])
        show_img = cv2.hconcat([show_img, frame_mesh_img])

        # Reset the NPC's HP and choose a new gesture if the HP is 0
        if npc_hp <= 0:
            npc_hp = 100
            next_guchokipa = ["gu", "choki", "pa"]
            next_guchokipa.remove(npc_jan)
            npc_jan = random.choice(next_guchokipa)
            janken_count += 1

        mouths = detector.get_mouth_xy()
        if len(mouths) > 0:
            mouth = mouths[0]
            put_str, your_jan = estimate_gesture(mouth)
            cv2.putText(show_img, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 8)
            cv2.putText(show_img, put_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            # Determine the winner of the janken game and update the NPC's HP
            if your_jan == "gu" and npc_jan == "choki":
                npc_hp -= 5
            elif your_jan == "choki" and npc_jan == "pa":
                npc_hp -= 5
            elif your_jan == "pa" and npc_jan == "gu":
                npc_hp -= 5
            janken_status_str = f"NPC HP:{npc_hp:3d} NPC:{npc_jan} vs YOU:{your_jan}"
            cv2.putText(show_img, janken_status_str, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 8)
            cv2.putText(show_img, janken_status_str, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            janken_count_str = str(janken_count)
            janken_count_position = (50, show_img.shape[0] - 50)
            cv2.putText(show_img, janken_count_str, janken_count_position, cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 12)
            cv2.putText(show_img, janken_count_str, janken_count_position, cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 4)

            image_top = 140
            image_left = 50
            image_gap = 30
            draw_gesture_image(show_img, gesture_images[npc_jan], (image_left, image_top), "NPC")
            if your_jan in gesture_images:
                your_image_left = image_left + gesture_image_size + image_gap
                draw_gesture_image(show_img, gesture_images[your_jan], (your_image_left, image_top), "YOU")

        cv2.imshow("cam", show_img)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord("s"):
            cv2.imwrite("photo.png", frame)
            print("saved photo.")
            break


def load_gesture_images():
    """Load the rock-paper-scissors images from the images directory."""
    images_dir = os.path.join(os.path.dirname(__file__), "images")
    gesture_images = {}

    for gesture in ("gu", "choki", "pa"):
        image_path = os.path.join(images_dir, f"{gesture}.png")
        image = cv2.imdecode(np.fromfile(image_path, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise FileNotFoundError(f"Could not load gesture image: {image_path}")
        gesture_images[gesture] = image

    return gesture_images


def draw_gesture_image(dst_img, gesture_img, top_left, label):
    """Draw a gesture image and its label at the specified position."""
    left, top = top_left
    height, width = gesture_img.shape[:2]
    bottom = top + height
    right = left + width

    dst_img[top:bottom, left:right] = gesture_img
    cv2.rectangle(dst_img, (left, top), (right - 1, bottom - 1), (255, 255, 255), 3)
    cv2.putText(dst_img, label, (left + 5, top + 21), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)


def estimate_gesture(mouth):
    """
    Calculate the distance between the mouth keypoints and determine the janken gesture.
    """
    distance_0_17 = ((mouth[0][0] - mouth[17][0]) ** 2 + (mouth[0][1] - mouth[17][1]) ** 2) ** 0.5
    distance_78_308 = ((mouth[78][0] - mouth[308][0]) ** 2 + (mouth[78][1] - mouth[308][1]) ** 2) ** 0.5
    ratio = distance_0_17 / distance_78_308
    if ratio < 0.4:
        janken = "gu"
    elif ratio > 1.5:
        janken = "choki"
    elif distance_0_17 > 100 and distance_78_308 > 100:
        janken = "pa"
    else:
        janken = "unknown"
    put_str = f"distance vertical:{distance_0_17:5.1f}, horizontal:{distance_78_308:5.1f}, ratio:{ratio:4.2f} ({janken})"
    return put_str, janken


if __name__ == "__main__":
    main()
