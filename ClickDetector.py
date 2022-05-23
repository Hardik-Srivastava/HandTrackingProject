import cv2 as cv
from time import sleep
from cvzone.HandTrackingModule import HandDetector

def main():
    cap = cv.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    click_No = 0
    detector = HandDetector(detectionCon=0.5)
    # For moving you  finger ahead
    # clickDistance = 20.1
    # For identifying by your finger moving down
    clickDistance = 5.1
    changeControl = False
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        if len(hands) == 1:
            lmList = hands[0]["lmList"]
            length, _ = detector.findDistance(lmList[4], lmList[8])
            # length1, _ = detector.findDistance(lmlist[8], lmlist[12])
            # length2, _ = detector.findDistance(lmlist[12], lmlist[16])
            # length3, _ = detector.findDistance(lmlist[16], lmlist[20])
            # length, info = detector.findDistance(lmList1[8], lmList1[12])
            # print("Length between 5 and 8:")
            # print(length)
            # print("Length between 5 and 6:")
            # print(length2)

            # For clicking via finger
            # if detector.fingersUp(hands[0]) == [0, 0, 0, 0, 0]:
            #     print('Click Detected')
            #     print(click_No)
            #     print(length)
            #     print('Click Ended')
            #     click_No += 1
            #     sleep(0.15)

            # for joining two adjacent fingers
            # if length < clickDistance:
            #     print('Click Detected')
            #     print(click_No)
            #     print(length)
            #     print('Click Ended')
            #     click_No += 1
            #     sleep(0.15)
            print(length)
            # for clicking as normal
            # if length < clickDistance:
            #     print('Click Detected')
            #     print(click_No)
            #     print(length)
            #     print('Click Ended')
            #     click_No += 1
            #     sleep(0.15)
            # if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 1]:
            #     changeControl = False
        cv.imshow("Image", img)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # if changeControl:
        #     if length1 < pauseDistance and length2 < pauseDistance and length3 < pauseDistance:
        #         cv.waitKey(1)
        #         break
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()