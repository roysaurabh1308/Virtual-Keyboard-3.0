# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temp orary script file.
"""
import cv2
import dlib
import numpy as np
from math import hypot
from playsound import playsound


cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

board= np.zeros((500,500),np.uint8)
board[:]=255

# Keyboard Settings
keyboard = np.zeros((450,750,3),np.uint8)
keys_set1 = {0:"Q",1:"W",2:"E",3:"R",4:"T",
             5:"A",6:"S",7:"D",8:"F",9:"G",
             10:"Z",11:"X",12:"C",13:"V",14:"<"}
keys_set2 = {0:"Y",1:"U",2:"I",3:"O",4:"P",
             5:"H",6:"J",7:"K",8:"L",9:"-",
             10:"B",11:"N",12:"M",13:",",14:"<"}


def letter(letter_index,text,letter_light):

    # Keys
    x=(letter_index%5)*150
    y=int(letter_index/5)*150

    height,width=150,150
    th= 3 #thickness
    if letter_light is True:
        cv2.rectangle(keyboard, (x+th,y+th), (x+width-th,y+height-th),(255,255,255),-1)
    else:

        cv2.rectangle(keyboard, (x+th,y+th), (x+width-th,y+height-th),(255,0,0),th)

    # Text-settings
    font_scale=8
    font_th =4
    font_letter =   cv2.FONT_HERSHEY_PLAIN
    text_size =cv2.getTextSize(text,font_letter,font_scale,font_th)[0]
    width_text, height_text = text_size[0],text_size[1]

    text_x= int((width-width_text)/2) +x
    text_y = int((height+height_text)/2) +y

    cv2.putText(keyboard,text,(text_x,text_y),font_letter,font_scale,(255,0,0),font_th)


def midpoint(p1,p2):
    return (int((p1.x+p2.x)/2),int((p1.y+p2.y)/2))

font = cv2.FONT_HERSHEY_PLAIN

def get_blinking_ratio(eye_points,facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x ,facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x ,facial_landmarks.part(eye_points[3]).y)

        center_top = midpoint(facial_landmarks.part(eye_points[1]),facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]),facial_landmarks.part(eye_points[4]))

        #hor_line = cv2.line(frame,left_point, right_point,(0,255,0),2)
        #ver_line = cv2.line(frame,center_top,center_bottom,(0,255, 0),2)

        hor_line_length = hypot((left_point[0]-right_point[0]),(left_point[1]-right_point[1]))
        ver_line_length = hypot((center_top[0]-center_bottom[0]),(center_top[1]-center_bottom[1]))

        ratio = hor_line_length/ver_line_length
        return ratio

def get_gaze_ratio(eye_points,facial_landmarks) :
        left_eye_region = np.array([(landmarks.part(eye_points[0]).x,landmarks.part(eye_points[0]).y),
                                    (facial_landmarks.part(eye_points[1]).x,facial_landmarks.part(eye_points[1]).y),
                                    (facial_landmarks.part(eye_points[2]).x,facial_landmarks.part(eye_points[2]).y),
                                    (facial_landmarks.part(eye_points[3]).x,facial_landmarks.part(eye_points[3]).y),
                                    (facial_landmarks.part(eye_points[4]).x,facial_landmarks.part(eye_points[4]).y),
                                    (facial_landmarks.part(eye_points[5]).x,facial_landmarks.part(eye_points[5]).y)],np.int32)
        #cv2.polylines(frame,[left_eye_region],True,(0,0,255),2)
        height,width,_ = frame.shape
        mask = np.zeros((height,width),np.uint8)

        cv2.polylines(mask,[left_eye_region],True,255,2)
        cv2.fillPoly(mask,[left_eye_region],255)
        eye = cv2.bitwise_and(gray,gray, mask=mask)

        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])

        gray_eye = eye[min_y:max_y, min_x:max_x]
        _,threshold_eye = cv2.threshold(gray_eye,55,255,cv2.THRESH_BINARY)
        height,width= threshold_eye.shape

        left_side_threshold= threshold_eye[0:height, 0: int(width/2)]
        left_side_white = cv2.countNonZero(left_side_threshold)

        right_side_threshold=threshold_eye[0:height, int(width/2):width]
        right_side_white = cv2.countNonZero(right_side_threshold)
        if right_side_white ==0:
            right_side_white =0.000001
        gaze_ratio = left_side_white/right_side_white
        return gaze_ratio

# Counter
count=0
letter_index=0
blinking_frames=0
sent=""
keyboard_selected = "left"
last_keyboard= "left"
keyboard_check=0
check_keyset =-1
active_letter= ""
while True :
    _,frame = cap.read()
    count+=1

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces :
        #x,y=face.left(), face.top()
        #x1,y1 = face.right(), face.bottom()
        #cv2.rectangle(frame,(x,y),(x1,y1),(0,255,0),2)

        landmarks= predictor(gray,face)

        # Detect Blinking
        left_eye_ratio = get_blinking_ratio([36,37,38,39,40,41],landmarks)
        right_eye_ratio = get_blinking_ratio([42,43,44,45,46,47],landmarks)
        blinking_ratio = (right_eye_ratio+left_eye_ratio)/2
        cv2.putText(frame,str(blinking_ratio),(200,100),font,2,(255,0,0),3)

        if blinking_ratio >4:
            cv2.putText(frame,"Blinking",(100,400),font,5,(0,0,255),4)
            blinking_frames+=1
            count-=1

            # Typing letter
            if blinking_frames==7:

                if active_letter =="<":
                    keyboard_check=0
                else:
                    if active_letter== "-":
                        active_letter=" "
                    sent+=active_letter
                    playsound('sound.wav')

        else:
            blinking_frames=0


        if keyboard_check==0:
            keyboard_check=1
            if keyboard_selected=="right":
                last_keyboard = "right"
                keyboard_selected="left"
                check_keyset=1
            else:
                last_keyboard = "left"
                keyboard_selected="right"
                check_keyset=0
            """
            # Gaze Detection
            gaze_ratio_left_eye = get_gaze_ratio([36,37,38,39,40,41],landmarks)
            gaze_ratio_right_eye = get_gaze_ratio([42,43,44,45,46,47],landmarks)

            gaze_ratio= (gaze_ratio_left_eye+gaze_ratio_right_eye)/2
            #cv2.putText(frame,str(gaze_ratio),(200,100),font,2,(255,0,0),3)
            if gaze_ratio < 0.8:
                cv2.putText(frame,"Right",(50,100),font,2,(0,0,255),3)
                keyboard_selected="right"
                if keyboard_selected !=last_keyboard:
                    playsound('right.wav')
                    last_keyboard="right"
                    keyboard_check=1
                    check_keyset=0

            elif 4 < gaze_ratio :
                cv2.putText(frame,"left",(50,100),font,2,(0,255,0),3)
                keyboard_selected="left"
                if keyboard_selected !=last_keyboard:
                    playsound('left.wav')
                    last_keyboard="left"
                    keyboard_check=1
                    check_keyset=1

            else :
                cv2.putText(frame,"Center",(50,100),font,2,(255,0,0),3)
            """

        """ threshold_eye = cv2.resize(threshold_eye,None,fx=5,fy=5)
        eye = cv2.resize(gray_eye,None,fx=5,fy=5)

        #cv2.imshow("Eye",eye)
        cv2.imshow("Threshold",threshold_eye)
        #cv2.imshow("Left eye",left_eye)
        cv2.imshow("Left",left_side_threshold)
        cv2.imshow("Right",right_side_threshold)"""

    if count==10:
        letter_index+=1
        keyboard[:] =(0,0,0)
        count=0
        if letter_index ==15:
            letter_index=0

    # Letters
    for i in range(15):
        if i==letter_index:
            light=True
        else :
            light=False

        if check_keyset==0:
            letter(i,keys_set2[i],light)
            active_letter = keys_set2[letter_index]

        elif check_keyset==1:
            letter(i,keys_set1[i],light)
            active_letter = keys_set1[letter_index]


    cv2.putText(board,sent,(10,100),font,4,0,3)

    cv2.imshow(" Virtual Keyboard",keyboard)
    cv2.imshow("Frame",frame)
    cv2.imshow("Board",board)

    key = cv2.waitKey(1)
    if key == 27 :
        break

cap.release()
cv2.destroyAllWindows()