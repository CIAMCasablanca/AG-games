import cv2
import numpy as np
import time
import os
import handtrackingmodule as htm


folderpath = "header"
canvas = np.zeros((720, 1280, 3), np.uint8)


heading = os.listdir(folderpath)

overlaylist = []
drawColor = [0, 0, 255]
brushSize = 15
eraserSize = 100

for img in heading:
    image = cv2.imread(f'{folderpath}\{img}')
    overlaylist.append(image)

header = overlaylist[1]

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


detector = htm.handDetector(mode=False, detectCon=0.85, trackCon=0.5)
xp, yp = 0, 0

pTime = 0
while True:

    isTrue, frame = cap.read()
    frame = cv2.flip(frame, 1)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    # 1. import images

    # 2. Find hand Landmarks
    frame = detector.findHands(frame)
    landmark_list = detector.findPos(frame)

    if len(landmark_list) != 0:

        x1, y1 = landmark_list[8][1:]
        x2, y2 = landmark_list[12][1:]

    # 3. Check which fingers are up

        fingers = detector.fingerUp()
        # print(fingers)

    # 4. Selection mode - If two fingers are up

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            if y1 < 125:
                if 230 < x1 < 450:
                    header = overlaylist[1]
                    drawColor = [0, 0, 255]
                elif 520 < x1 < 700:
                    header = overlaylist[2]
                    drawColor = [0, 255, 0]

                elif 750 < x1 < 950:
                    header = overlaylist[3]
                    drawColor = [255, 0, 0]
                elif 1020 < x1 < 1200:
                    header = overlaylist[4]
                    drawColor = [0, 0, 0]
            # cv2.rectangle(frame, (x1, y1-15), (x2, y2+15), drawColor, cv2.FILLED)
            # cv2.rectangle(canvas, (x1, y1-15), (x2, y2+15), drawColor, cv2.FILLED)

        # 5. Drawing mode - If one finger is up.

        if (fingers[1] and fingers[2]) == False:
            cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(frame, (xp, yp), (x1, y1), drawColor, eraserSize)
                cv2.line(canvas, (xp, yp), (x1, y1), drawColor, eraserSize)
            else:
                cv2.line(frame, (xp, yp), (x1, y1), drawColor, brushSize)
                cv2.line(canvas, (xp, yp), (x1, y1), drawColor, brushSize)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, imgInv)
    frame = cv2.bitwise_or(frame, canvas)

    frame[0:125, 0:1280] = header

    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    cv2.imshow('frame', frame)
    cv2.putText(frame, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)
    #cv2.imshow('canvas', canvas)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
