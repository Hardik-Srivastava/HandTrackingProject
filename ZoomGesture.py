import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
startDistance = None
scale = 0
cx, cy = 640, 360
img1 = cv.imread('Images/galaxy.jpg')
while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img1 = cv.imread('Images/galaxy.jpg')
    hands, img = detector.findHands(img)
    if len(hands) == 2:
        if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0] and detector.fingersUp(hands[1]) == [0, 1, 0, 0, 0]:
            print('Zoom Gesture')
            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            if startDistance is None:
                length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                print(length)
                startDistance = length
            length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
            scale = int((length - startDistance)//2)
            print(scale)
            cx, cy = info[4:]
    else:
        startDistance = None
        scale = 0
    h1, w1, _ = img1.shape
    newH, newW = (((h1 + scale) // 2) * 2), (((w1 + scale) // 2) * 2)
    img1 = cv.resize(img1, (newW, newH))
    img[cy-newH//2:cy+newH//2, cx-newW//2:cx+newW//2] = img1
    cv.imshow("Image", img)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cv.destroyAllWindows()
