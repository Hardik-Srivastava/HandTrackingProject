import cv2 as cv
import numpy as np
import pyautogui
import time
from time import sleep
from cvzone.HandTrackingModule import HandDetector


def main():
    cap = cv.VideoCapture(0)
    wCam, hCam = 1440, 810
    wScreen, hScreen = pyautogui.size()
    cap.set(3, wCam)
    cap.set(4, hCam)
    frameR = 200
    clickDistance = 28.1
    pauseDistance = 29
    changeControl = False
    dragClick = False
    smoothening = 1
    pLocX, pLocY = 0, 0
    cLocX, cLocY = 0, 0
    pTime = 0
    cTime = 0
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        if hands:
            cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
            lmlist = hands[0]["lmList"]
            length, _ = detector.findDistance(lmlist[8], lmlist[4])
            length1, _ = detector.findDistance(lmlist[8], lmlist[12])
            length2, _ = detector.findDistance(lmlist[12], lmlist[16])
            length3, _ = detector.findDistance(lmlist[16], lmlist[20])
            x = np.interp(lmlist[5][0], (frameR, wCam - frameR), (0, 1920))
            y = np.interp(lmlist[5][1], (frameR, hCam - frameR), (0, 1080))
            cLocX = pLocX + (x - pLocX) / smoothening
            cLocY = pLocY + (y - pLocY) / smoothening
            # print(x, y)
            pyautogui.moveTo(cLocX, cLocY)
            # Clicking
            if length < clickDistance:
                pyautogui.click()
                print("Clicked")
                sleep(0.15)
            # Dragging and clicking
            if dragClick and length < clickDistance:
                pyautogui.dragTo(cLocX, cLocY)

            # Changing control for Drag
            if detector.fingersUp(hands[0]) == [0, 0, 0, 0, 0]:
                if dragClick:
                    print('Drag is off')
                    dragClick = False
                else:
                    print('Drag is on')
                    dragClick = True

            # Changing control for closing python console
            if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 1]:
                print('Changed Control')
                changeControl = True

            # Scrolling the Window
            if detector.fingersUp(hands[0]) == [0, 1, 1, 1, 0]:
                pyautogui.scroll(3, cLocX, cLocY)
                pLocX, pLocY = cLocX, cLocY
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv.imshow("Image", img)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if changeControl:
            if length1 < pauseDistance and length2 < pauseDistance and length3 < pauseDistance:
                cv.waitKey(1)
                break
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
