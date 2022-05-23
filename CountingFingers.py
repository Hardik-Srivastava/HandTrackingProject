import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import HandTrackingModule as htm

def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector = htm.HandDetector(detectionCon=0.75)
    tipIds = [4, 8, 12, 16, 20]
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        fingers = []
        if len(lmList) != 0:
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        print(fingers)
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv.imshow("Image", img)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()