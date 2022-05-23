import csv
import cv2 as cv
import mediapipe as mp
import cvzone
from time import sleep
from cvzone.HandTrackingModule import HandDetector
class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, img, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x+1
                img = cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2, cv.FILLED)
        return img


def main():
    cap = cv.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    clickDistance = 28.1
    pauseDistance = 29
    changeControl = False
    detector = HandDetector(detectionCon=0.5)
    pathCSV = "Mcqs.csv"
    with open(pathCSV, newline='\n') as f:
        reader = csv.reader(f)
        dataAll = list(reader)[1:]

    # Create object for each MCQ
    mcqList = []
    for q in dataAll:
        mcqList.append(MCQ(q))
    # print(dataAll)
    qNo = 0
    qData = len(dataAll)
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        if qNo < qData:
            mcq = mcqList[qNo]
            img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5)
            img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
            img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
            img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
            img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)
            if hands:
                lmlist = hands[0]["lmList"]
                cursor = lmlist[5]
                length, _ = detector.findDistance(lmlist[8], lmlist[4])
                length1, _ = detector.findDistance(lmlist[8], lmlist[12])
                length2, _ = detector.findDistance(lmlist[12], lmlist[16])
                length3, _ = detector.findDistance(lmlist[16], lmlist[20])
                if length < clickDistance:
                    img = mcq.update(img, cursor, [bbox1, bbox2, bbox3, bbox4])
                    if mcq.userAns != None:
                        sleep(0.15)
                        print(mcq.userAns)
                        qNo += 1
        else:
            score = 0
            for mcq in mcqList:
                if mcq.answer == mcq.userAns:
                    score += 1
            score = round((score/qData)*100, 2)
            img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
            img, _ = cvzone.putTextRect(img, f'Your score:{score}%', [700, 300], 2, 2, offset=50, border=5)
        # Draw Progress Bar
        barValue = 150 + (950//qData)*qNo
        cv.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv.FILLED)
        cv.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
        img, _ = cvzone.putTextRect(img, f'{round((qNo/qData)*100)}%', [1130, 635], 2, 2, offset=50, border=5)
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
