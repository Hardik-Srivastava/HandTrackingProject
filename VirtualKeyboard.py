import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<-" ],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]


class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text


def main():
    # wScreen, hScreen = pyautogui.size()
    # wCam, hCam = 1280, 720
    # frameR = 200
    pauseDistance = 29
    length1 = 200.555
    length2 = 200.555
    length3 = 200.555
    cap = cv.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)
    keyboard = Controller()
    changeControl = False
    buttonList = []
    clickDistance = 28.1
    finalText = ""
    clickedText = ""
    intialClick = False
    # print([wScreen, hScreen])
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            if key != "<-":
                buttonList.append(Button([j * 100 + 50, 100 * i + 50], key))
            else:
                buttonList.append(Button([j * 100 + 50, 100 * i + 50], key, (125, 85)))
    detector = HandDetector(detectionCon=0.5)

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        hands, img = detector.findHands(img, flipType = False)
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            cv.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv.FILLED)
            cv.putText(img, button.text, (x + 20, y + 65), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        cv.rectangle(img, (50, 500), (700, 600), (175, 0, 175), cv.FILLED)
        cv.putText(img, finalText, (60, 575), cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
        if len(hands) == 1:
            # cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
            lmList = hands[0]["lmList"]
            length1, _ = detector.findDistance(lmList[8], lmList[12])
            length2, _ = detector.findDistance(lmList[12], lmList[16])
            length3, _ = detector.findDistance(lmList[16], lmList[20])
            pointer_x = lmList[8][0]
            pointer_y = lmList[8][1]
            # pointer_x = np.interp(lmList[8][0], (frameR, wCam - frameR), (0, wScreen))
            # pointer_y = np.interp(lmList[8][1], (frameR, hCam - frameR), (0, hScreen))
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                if x < pointer_x < (x + h) and y < pointer_y < (y + h):
                    cv.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv.FILLED)
                    cv.putText(img, button.text, (x + 20, y + 65), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    # When Clicked
                    if length1 < clickDistance:
                        cv.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv.FILLED)
                        cv.putText(img, button.text, (x + 20, y + 65), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        if button.text == "<-":
                            if finalText != "":
                                finalText = finalText[0:(len(finalText)-1)]
                        else:
                            # pynput.press(clickedText)
                            finalText += button.text
                        sleep(0.15)
            if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 1]:
                print('Changed control')
                changeControl = True
        cv.imshow("Image", img)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if changeControl:
            if length1 < pauseDistance and length2 < pauseDistance and length3 < pauseDistance:
                cv.waitKey(1)
                break
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
