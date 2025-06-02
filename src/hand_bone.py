import cv2
import mediapipe as mp


class HandLandMarks:
    def __init__(self, staticMode=False, max_hands=1, minDetectionCon=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.max_hands = max_hands
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hand_bones = self.mp_hands.Hands(
            self.staticMode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.minDetectionCon,
            min_tracking_confidence=self.minTrackCon,
        )
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

    def find_hand_keypoints(self, src_img):
        self.imgRGB = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
        self.results = self.hand_bones.process(self.imgRGB)

        self.hands = []

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                hand = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    ih, iw, ic = src_img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    hand.append([x, y])
                self.hands.append(hand)

    def draw(self, src_img):
        dst_img = src_img.copy()
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    dst_img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=self.drawSpec,
                    connection_drawing_spec=self.drawSpec,
                )
        return dst_img

    def get_all_xy(self):
        return self.hands

    def get_hand_xy(self):
        hands = []
        for hand in self.hands:
            hands.append({i: hand[i] for i in [0, 4, 8, 12, 16, 20]})
        return hands
