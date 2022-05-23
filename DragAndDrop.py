import cv2 as cv
from cvzone.HandTrackingModule import HandDetector


def main():
    cap = cv.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector()
    img1 = cv.imread('Images/galaxy.jpg')
    clickDistance = 28.1
    pauseDistance = 29
    changeControl = False
    ox, oy = 640, 360
    h, w, _ = img1.shape
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        if hands:
            lmlist = hands[0]["lmList"]
            length1, _ = detector.findDistance(lmlist[8], lmlist[12])
            length2, _ = detector.findDistance(lmlist[12], lmlist[16])
            length3, _ = detector.findDistance(lmlist[16], lmlist[20])
            if length1 < clickDistance:
                x, y = lmlist[8][0], lmlist[8][1]
                if ox < x < ox + w and oy < y < oy + h:
                    ox, oy = lmlist[8][0] - w // 2, lmlist[8][1] - h // 2
            if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 1]:
                print('Changed Control')
                changeControl = True
        img[oy:oy + h, ox:ox + w] = img1
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
