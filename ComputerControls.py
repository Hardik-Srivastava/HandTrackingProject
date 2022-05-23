import cv2 as cv
import numpy as np
import pyautogui
import time
from time import sleep

import pynput.keyboard
from pynput.keyboard import Controller
from cvzone.HandTrackingModule import HandDetector


def main():
    cap = cv.VideoCapture(0)
    wCam, hCam = 1440, 810
    wScreen, hScreen = pyautogui.size()
    cap.set(3, wCam)
    cap.set(4, hCam)
    frameR = 200
    dragOn = False
    clickDistance = 28.1
    pauseDistance = 29
    changeControl = False
    closeProgram = False
    scrollOn = False
    closingWindows = False
    dragClick = False
    changeWindows = False
    firstChange = False
    smoothening = 1
    pLocX, pLocY = 0, 0
    cLocX, cLocY = 0, 0
    pTime = 0
    cTime = 0
    keyboard = Controller()
    detector = HandDetector(detectionCon=0.75)
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        hands, img = detector.findHands(img, flipType=True)
        if hands:
            cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
            myHands = hands
            for hand in myHands:
                if hand["type"] == "Left":
                    break
            for righthand in myHands:
                if righthand["type"] == "Right":
                    rightlmlist=righthand["lmList"]
                    break
            lmlist = hand["lmList"]
            length, _ = detector.findDistance(lmlist[8], lmlist[4])
            length1, _ = detector.findDistance(lmlist[8], lmlist[12])
            length2, _ = detector.findDistance(lmlist[12], lmlist[16])
            length3, _ = detector.findDistance(lmlist[16], lmlist[20])
            length4, _ = detector.findDistance(lmlist[4], lmlist[12])
            if detector.fingersUp(hand) == [0, 1, 0, 0, 0] or detector.fingersUp(hand) == [1, 1, 0, 0, 0]:
                x = np.interp(lmlist[5][0], (frameR, wCam - frameR), (0, 1920))
                y = np.interp(lmlist[5][1], (frameR, hCam - frameR), (0, 1080))
                cLocX = pLocX + (x - pLocX) / smoothening
                cLocY = pLocY + (y - pLocY) / smoothening
                # print(x, y)
                pyautogui.moveTo(cLocX, cLocY)
                pLocX, pLocY = cLocX, cLocY
                if length < clickDistance:
                    pyautogui.click()
                    print("Clicked")
                    sleep(0.15)
            if not changeWindows:
                if detector.fingersUp(hand) == [0, 1, 1, 0, 0] and length1 > clickDistance:
                    pyautogui.keyDown('altleft')
                    pyautogui.keyDown('tab')
                    pyautogui.keyUp('tab')
                    changeWindows = True
            if changeWindows:
                if not firstChange:
                    if detector.fingersUp(hand) == [0, 1, 1, 0, 0]:
                        firstChange = True
                else:
                    if detector.fingersUp(hand) == [0, 1, 0, 0, 0]:
                        firstChange = False
                        pyautogui.keyDown('tab')
                        pyautogui.keyUp('tab')
                    if detector.fingersUp(hand) == [0, 0, 0, 0, 0]:
                        closingWindows = False
                        changeWindows = False
                        pyautogui.keyUp('altleft')
            if righthand["type"] == "Right" and hand:
                ry = rightlmlist[3][1]
                ly = lmlist[5][1]
                if detector.fingersUp(righthand) == [1, 0, 0, 0, 0]:
                    if ry < ly:
                        pyautogui.press('up')
                    else:
                        pyautogui.press('down')

            if righthand:
                if righthand["type"] == "Right":
                    if detector.fingersUp(righthand) == [0, 1, 0, 0, 1]:
                        print('Changed control')
                        changeControl = True
            if changeControl:
                if hand:
                    if hand["type"] == "Left":
                        if detector.fingersUp(hand) == [0, 1, 0, 0, 1]:
                            print('Close program')
                            cv.waitKey(1)
                            break
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv.imshow("Image", img)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
