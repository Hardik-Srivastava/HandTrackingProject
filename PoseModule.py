import cv2 as cv
import mediapipe as mp
import numpy as np
import time
class poseDetector:
    def __init__(self, mode=False, upBody = False, smooth=True, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth=smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        #self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        # print(self.results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=False):
        lmlist = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 8, (255, 0, 255), cv.FILLED)
        return lmlist


def main():
    cap = cv.VideoCapture('PoseVideos/KamariyaChoreography.mp4')
    detector = poseDetector()
    pTime = 0
    while True:
        success, img = cap.read()
        # img = cv.flip(img, 1)
        img = detector.findPose(img)
        # lmlist = detector.findPosition(img)
        # if len(lmlist) != 0:
        #     print(lmlist[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv.imshow("Video", img)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
