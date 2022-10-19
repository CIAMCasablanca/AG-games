#points LeftElbow  = 13, RightElbow = 14 , LeftPalm = 15 , RightPalm = 16
'''
To play you should first install The packages imported (using pip install "package"):
   - pygame
   - mediapipe
   - cv2
Then start The game and it will open your camera automatically and a game window .
Game Rules:
   - To move The snake up, rise both of your hands up.
   - To move The snake down, lower both of your hands down.
   - To move The snake right, rise your right hand and lower your left hand.
   - To move The snake left, rise your left hand and lower yourright hand.
   + The more score you get The greater You are (Try beat my score 12)
   + Enjoy :)
'''
import cv2
import mediapipe as mp
import time
import math
from PoseModule import poseDetector
import pygame
import random
#### game settings #########
pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 10, 10) # well kinda black
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dir = ''

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game ')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10


font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
########################
#### functions #######
def Your_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

####################


def hand_direction(lmList, img):
    if len(lmList) != 0:
        global dir
        dir = ''
        # print(lmList[14],"\t",lmList[13],"\t",lmList[16],"\t",lmList[15])
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (lmList[13][1], lmList[13][2]), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (lmList[15][1], lmList[15][2]), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (lmList[16][1], lmList[16][2]), 10, (0, 0, 255), cv2.FILLED)
        if lmList[14][2] > lmList[16][2] and lmList[13][2] > lmList[15][2]:
            dir+='u'
            print("up")
        if lmList[13][2] > lmList[15][2] and lmList[14][2] < lmList[16][2]:
            dir += 'l'
            print("left")
        if lmList[14][2] < lmList[16][2] and lmList[13][2] < lmList[15][2]:
            dir += 'd'
            print("down")
        if lmList[13][2] < lmList[15][2] and lmList[14][2] > lmList[16][2]:
            dir += 'r'
            print("right")


def move_snake(dir,x1_change,y1_change,snake_block):
    if dir == 'l':
        x1_change = -snake_block
        y1_change = 0
    elif dir == 'r':
        x1_change = snake_block
        y1_change = 0
    elif dir == 'u':
        y1_change = -snake_block
        x1_change = 0
    elif dir == 'd':
        y1_change = snake_block
        x1_change = 0

def main():
    ###### more game settings #####
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    ################
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()
    while not game_over:
        global dir
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main()
        ##### mediapipe shit #######
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        hand_direction(lmList, img)



        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        img = cv2.flip(img,1)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        ############ #############
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        ### image verification
        if dir == 'l':
            x1_change = -snake_block
            y1_change = 0
        elif dir == 'r':
            x1_change = snake_block
            y1_change = 0
        elif dir == 'u':
            y1_change = -snake_block
            x1_change = 0
        elif dir == 'd':
            y1_change = snake_block
            x1_change = 0
        print(dir)


        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
