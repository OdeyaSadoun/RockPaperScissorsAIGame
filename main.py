"""
ROCK PAPER AND SCISSORS GAME
By:
    Nov Segal                   209550847
    Odeya Sadoun                212380406
    Tamar Gavrieli-Ben Eliyahu  322533977
    Yael Adler                  322877903
"""

import cv2
import time
import os
import HandTrackingModule as htm
import random


wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

timeUp = 5

# Credit on images to Vecteezy.com
# "https://www.vecteezy.com/free-vector/two-hands" Two Hands Vectors by Vecteezy :
folderPath = "ExitAndStartImages"
myListExitAndStart = os.listdir(folderPath)
ExitAndStartImagesList = []
for imPath in myListExitAndStart:
    image = cv2.imread(f'{folderPath}/{imPath}')
    ExitAndStartImagesList.append(image)
hExit, wExit, cExit = ExitAndStartImagesList[0].shape
hStart, wStart, cStart = ExitAndStartImagesList[1].shape

# "https://www.vecteezy.com/free-vector/rock-paper-scissors" Rock Paper Scissors Vectors by Vecteezy :
folderPath = "PRSImages"
myListPRS = os.listdir(folderPath)
PRSImagesList = []
for imPath in myListPRS:
    image = cv2.imread(f'{folderPath}/{imPath}')
    PRSImagesList.append(image)
hPaper, wPaper, cPaper = PRSImagesList[0].shape
hRock, wRock, cRock = PRSImagesList[1].shape
hScissors, wScissors, cScissors = PRSImagesList[2].shape
hSpace, wSpace = 50, 30



"""
Captures a frame from the camera, and returns this frame and the hands' landmarks that's in this frame
"""
def captureLandmarksInFrame():
    success, img = cap.read()  # read the frame
    img = cv2.flip(img, 1)  # mirror the frame
    img, num_hands_detected = detector.findHands(img, draw=False)  # find the hands
    landmarksList = detector.findPosition(img, draw=False)  # create the hands' landmarks
    return img, num_hands_detected, landmarksList


"""
When the user puts his hand in front of the camera, analyses his choice:
    paper = 1
    rock = 2
    scissors = 3
    none of the above = 0
"""
def analyseUserChoice(landmarksList):
    fingers = []
    # Thumb
    if landmarksList[tipIds[0]][1] < landmarksList[tipIds[4] - 1][1]:  # right hand
        if landmarksList[tipIds[0]][1] < landmarksList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    else:  # left hand
        if landmarksList[tipIds[0]][1] > landmarksList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    # 4 Fingers
    for id in range(1, 5):
        if landmarksList[tipIds[id]][2] < landmarksList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    totalFingers = fingers.count(1)  # the number of fingers

    if totalFingers == 5:  # paper
        return 1
    elif totalFingers == 0:  # rock
        return 2
    elif totalFingers == 2 and fingers[1] == 1 and fingers[2] == 1:  # scissors
        return 3
    return 0


"""
Gets the user's choice and shows the suitable image on the upper left corner of the screen
"""
def showUserChoice(img, userChoice):
    if userChoice == 1:  # paper
        cv2.putText(img, "USER", (wSpace + 30, hSpace - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 193, 43), 2)
        img[hSpace:hSpace + hPaper, wSpace:wSpace + wPaper] = PRSImagesList[0]
    elif userChoice == 2:  # rock
        cv2.putText(img, "USER", (wSpace + 30, hSpace - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (186, 108, 255), 2)
        img[hSpace:hSpace + hRock, wSpace:wSpace + wRock] = PRSImagesList[1]
    elif userChoice == 3:  # scissors
        cv2.putText(img, "USER", (wSpace + 30, hSpace - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (57, 229, 255), 2)
        img[hSpace:hSpace + hScissors, wSpace:wSpace + wScissors] = PRSImagesList[2]


"""
Ruffles the computer's choice:
    paper = 1
    rock = 2
    scissors = 3
And shows the suitable image on the upper right corner of the screen
"""
def ruffleAndShowComputerChoice(img):
    computerChoice = random.randint(1, 3)

    if computerChoice == 1:  # paper
        cv2.putText(img, "COMPUTER", (wCam - wPaper - wSpace - 5, hSpace - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 193, 43), 2)
        img[hSpace:hSpace + hPaper, wCam - wSpace - wPaper:wCam - wSpace] = PRSImagesList[0]
    elif computerChoice == 2:  # rock
        cv2.putText(img, "COMPUTER", (wCam - wRock - wSpace - 5, hSpace - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (186, 108, 255), 2)
        img[hSpace:hSpace + hRock, wCam - wSpace - wRock:wCam - wSpace] = PRSImagesList[1]
    elif computerChoice == 3:  # scissors
        cv2.putText(img, "COMPUTER", (wCam - wScissors - wSpace - 5, hSpace - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (57, 229, 255), 2)
        img[hSpace:hSpace + hScissors, wCam - wSpace - wScissors:wCam - wSpace] = PRSImagesList[2]

    return computerChoice


"""
Given the user's and the computer's choices, the function finds the winner and shows it on the screen
The winning-losing options are:
    -----------------------------
    WINNER      |   LOSER
    ------------+----------------
    paper = 1   |   rock = 2
    rock = 2    |   scissors = 3
    scissors = 3|   paper = 1
    -----------------------------
Therefore the next equation holds: (WINNER + 1) % 3 == LOSER % 3
"""
def findAndShowWinner(img, userChoice, computerChoice):
    winner = "T"
    if (computerChoice + 1) % 3 == userChoice % 3:
        winner = "C"
    elif (userChoice + 1) % 3 == computerChoice % 3:
        winner = "U"

    if winner == "C":
        cv2.putText(img, "You Lose!", (203, 100), cv2.FONT_HERSHEY_PLAIN, 3, (14, 2, 203), 5)
    elif winner == "U":
        cv2.putText(img, "You Win!", (211, 100), cv2.FONT_HERSHEY_PLAIN, 3, (22, 166, 0), 5)
    else:
        cv2.putText(img, "It's a Tie!", (201, 100), cv2.FONT_HERSHEY_PLAIN, 3, (31, 198, 255), 5)


def main(rec=0):
    onePaperSignFrameCounter = 0
    twoHandsFrameCounter = 0
    while True:
        img, num_hands_detected, landmarksList = captureLandmarksInFrame()
        if rec == 0:
            cv2.putText(img, "WELCOME:)", (140, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (31, 198, 255), 5)
            cv2.putText(img, "WELCOME:)", (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 2, (134, 68, 6), 5)
        else:
            cv2.putText(img, "Try Again", (144, 104), cv2.FONT_HERSHEY_SIMPLEX, 2, (31, 198, 255), 5)
            cv2.putText(img, "Try Again", (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 2, (134, 68, 6), 5)
        img[hCam - hExit:hCam, wCam - wExit:wCam] = ExitAndStartImagesList[0]
        img[hCam - hStart:hCam, 0:wStart] = ExitAndStartImagesList[1]

        if num_hands_detected == 2:
            onePaperSignFrameCounter = 0
            twoHandsFrameCounter += 1
            if twoHandsFrameCounter >= 20:
                time.sleep(1)
                return
        elif num_hands_detected == 1:
            twoHandsFrameCounter = 0
            userSign = analyseUserChoice(landmarksList)
            if userSign == 1:
                onePaperSignFrameCounter += 1
                if onePaperSignFrameCounter >= 10:
                    break
            else:
                onePaperSignFrameCounter = 0
        else:
            onePaperSignFrameCounter = 0
            twoHandsFrameCounter = 0
        cv2.imshow("Rock Paper Scissors Game", img)
        cv2.waitKey(1)

    # A game starts - counting down till the decision time:
    t_now = time.time()
    t_end = t_now + timeUp
    while t_now < t_end:
        img, num_hands_detected, landmarksList = captureLandmarksInFrame()
        if num_hands_detected == 2:
            cv2.putText(img, "Show only ONE hand", (wSpace + 30, hSpace - 5),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        elif num_hands_detected == 1:
            userChoice = analyseUserChoice(landmarksList)
            if userChoice == 0:
                cv2.putText(img, "Make your choice!", (wSpace + 30, hSpace - 5),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            else:
                showUserChoice(img, userChoice)
        else:
            cv2.putText(img, "Make your choice!", (wSpace + 30, hSpace - 5),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        rgb = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
        cv2.putText(img, str(int(t_end - t_now) + 1), (wCam - 150, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, rgb, 12)
        cv2.imshow("Rock Paper Scissors Game", img)
        cv2.waitKey(1)
        t_now = time.time()

    # Time's Up! Analyse results:
    img, num_hands_detected, landmarksList = captureLandmarksInFrame()
    if num_hands_detected >= 2:
        cv2.putText(img, "Too Many Hands!", (125, 100), cv2.FONT_HERSHEY_PLAIN, 3, (134, 68, 6), 5)
    elif num_hands_detected == 1:
        userChoice = analyseUserChoice(landmarksList)
        if userChoice == 0:
            cv2.putText(img, "Rock Paper or Scissors ONLY", (70, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (134, 68, 6), 3)
        else:
            showUserChoice(img, userChoice)
            computerChoice = ruffleAndShowComputerChoice(img)
            findAndShowWinner(img, userChoice, computerChoice)
    else:
        cv2.putText(img, "No Hands.....!", (155, 100), cv2.FONT_HERSHEY_PLAIN, 3, (134, 68, 6), 5)

    cv2.imshow("Rock Paper Scissors Game", img)
    cv2.waitKey(1)
    time.sleep(3)
    main(rec+1)


if __name__ == "__main__":
    main()

