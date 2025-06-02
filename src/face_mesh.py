import cv2
import mediapipe as mp


class FaceLandMarks:
    def __init__(self, staticMode=False, maxFace=1, minDetectionCon=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.maxFace = maxFace
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(
            self.staticMode,
            refine_landmarks=True,
            max_num_faces=self.maxFace,
            min_detection_confidence=self.minDetectionCon,
            min_tracking_confidence=self.minTrackCon,
        )
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

    def find_face_keypoints(self, src_img):
        self.imgRGB = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)

        self.faces = []

        if self.results.multi_face_landmarks:
            for face_landmarks in self.results.multi_face_landmarks:
                face = []
                for id, lm in enumerate(face_landmarks.landmark):
                    ih, iw, ic = src_img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    face.append([x, y])
                self.faces.append(face)

    def draw(self, src_img):
        if self.results.multi_face_landmarks:
            for face_landmarks in self.results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(
                    src_img,
                    face_landmarks,
                    self.mpFaceMesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=self.drawSpec,
                    connection_drawing_spec=self.drawSpec,
                )
        return src_img

    def get_all_xy(self):
        return self.faces

    def get_mouth_xy(self):
        mouths = []
        for face in self.faces:
            mouths.append({i: face[i] for i in [0, 13, 14, 17, 61, 78, 291, 308]})
        return mouths
