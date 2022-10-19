import cv2
import mediapipe as mp
import time


class handDetector():

    def __init__(self, mode=False, maxhands=1,modelComplexity=1, detectCon=0.6, trackCon=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.modelComplex=modelComplexity
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxhands,self.modelComplex, self.detectCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, frame, draw=True):

        RGBimg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(RGBimg)

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        frame, handLMS, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPos(self, frame, handNo=0, draw=False):

        self.landmark_list = []

        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):

                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)

                self.landmark_list.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

        return self.landmark_list

    def fingerUp(self):

        fingers = []
        if len(self.landmark_list) != 0:

            # Thumb
            if self.landmark_list[self.tipIds[0]][1] < self.landmark_list[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):

                if self.landmark_list[self.tipIds[id]][2] < self.landmark_list[self.tipIds[id] - 2][2]:
                    fingers.append(1)

                else:
                    fingers.append(0)

        # print(fingers)

        return fingers


def main():

    cap = cv2.VideoCapture(0)

    pTime = 0

    detector = handDetector()

    while True:
        isTrue, frame = cap.read()

        # print(frame.shape)

        frame = detector.findHands(frame)
        landmark_list = detector.findPos(frame)
        f = detector.fingerUp()

        # if len(landmark_list) != 0:
        #     print(landmark_list[4])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)

        cv2.imshow('frame', frame)

        if cv2.waitKey(20) & 0xff == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


# if we are running the script then run this:
if __name__ == '__main__':
    main()
