import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector


def main():
    cap = cv.VideoCapture(0)
    wCam, hCam = 1280, 720
    cap.set(3, wCam)
    cap.set(4, hCam)
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    clickDistance = 20.1

    brushThickness = 15
    drawColor = (255, 0, 255)
    xp, yp = 0, 0
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        if hands:
            lmlist = hands[0]["lmList"]
            x1, y1 = lmlist[5]
            length, _ = detector.findDistance(lmlist[8], lmlist[4])
            if length<clickDistance:
                cv.circle(img, (x1, y1), 5, drawColor, cv.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                cv.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                xp, yp = x1, y1
            else:
                xp, yp = x1, y1

        img=cv.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
        cv.imshow("Image", img)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
