import cv2
import numpy as np
import copy
import math
from pythonosc import osc_message_builder
from pythonosc import udp_client
client = udp_client.SimpleUDPClient('127.0.0.1', 57120)


# parameters
threshold = 60  #  BINARY threshold
blurValue = 31  # GaussianBlur parameter   #original 41
bgSubThreshold = 50
learningRate = 0

# variables
isBgCaptured = 0   # bool, whether the background captured

2

# bass parameters
count_bass=0
x_bass_min=300
x_bass_max=450
y_bass_min=550//2
y_bass_max=700//2

# snare parameters
count_snare=0
x_snare_min=900//2
x_snare_max=1200//2
y_snare_min=550//2
y_snare_max=700//2



# Manually set up our ROI for grabbing the hand.
# Feel free to change these. I just chose the top right corner for filming.
roi_top = 30
roi_bottom = 280
roi_right = 30
roi_left = 240




def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


   
 #------------- COUNT FINGER FUNCTION ------------


def calculateFingers(res,drawing):  # -> finished bool, cnt: finger count
    #  convexity defect
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None):  # avoid crashing 

            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            return True, cnt
    return False, 0



##  ---------- MAIN------------

cam = cv2.VideoCapture(0)
cam.set(3,600)
cam.set(4,480)
cam.set(5,25)

cv2.namedWindow('trackbar')
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)

# Intialize a frame count
num_frames = 0
stop1=0
stop2=0
stop3=0
stop_drum1=0
stop_drum2=0
stop_seq1=0
stop_seq2=0
stop_seq3=0


x_pos_yellow=0
y_pos_yellow=0

count=0
stop_count1=0
stop_count2=0
finger_val=False

# keep looping, until interrupted
while True:
    # get the current frame
    ret, frame = cam.read()
    threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter

    # flip the frame so that it is not the mirror view
    frame = cv2.flip(frame, 1)

    # clone the frame
    frame_copy = frame.copy()
    blend2=frame_copy.copy()
    
    # --------------------DRUM COLOR FUNCTION --------------------
    
    
    hsv=cv2.cvtColor(frame_copy,cv2.COLOR_BGR2HSV)
    
    blue_lower= np.array([88,158,124],np.uint8)
    blue_upper= np.array([138,255,255],np.uint8)
    yellow_lower=np.array([21,39,64],np.uint8) # nigth=22,60,200   day=22,60,100
    yellow_upper=np.array([40,255,255],np.uint8)  
    green_lower=np.array([41,39,64],np.uint8)  # nigth=64,100,150    day=64,100,70
    green_upper=np.array([80,255,255],np.uint8)
    
    blue=cv2.inRange(hsv,blue_lower,blue_upper)
    green=cv2.inRange(hsv,green_lower,green_upper)
    yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)
    
    kernel=np.ones([5,5],"uint8")
    
    blue = cv2.morphologyEx(blue, cv2.MORPH_OPEN, kernel)
    blue = cv2.morphologyEx(blue, cv2.MORPH_CLOSE, kernel)
    yellow = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel)
    yellow = cv2.morphologyEx(yellow, cv2.MORPH_CLOSE, kernel)  
    green = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
    green = cv2.morphologyEx(green, cv2.MORPH_CLOSE, kernel)
    
    im2, contours, hierarchy = cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)        
    for pic,contour in enumerate(contours):
        area=cv2.contourArea(contour)
        if (area>300):
            x,y,w,h=cv2.boundingRect(contour)
            img=cv2.rectangle(frame_copy,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img,"",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,255,0))
            
            x_pos_yellow=x
            y_pos_yellow=y
            

            if (x>x_bass_min)and(x<x_bass_max)and(y>y_bass_min)and(y<y_bass_max)and(stop_drum1==0):
                    
                msg= osc_message_builder.OscMessageBuilder(address="/first")     
                msg.add_arg(44,arg_type ='i')
                msg.add_arg(0,arg_type ='i')
                msg.add_arg(0,arg_type ='i')
                msg=msg.build()
                client.send_message('/first',msg) 
                stop_drum1=1
                stop_drum2=0
                stop_seq1=0
                stop_seq2=0
                stop_seq3=0
                

            if (x>x_snare_min)and(x<x_snare_max)and(y>y_snare_min)and(y<y_snare_max)and(stop_drum2==0):
                    
                msg= osc_message_builder.OscMessageBuilder(address="/first")     
                msg.add_arg(66,arg_type ='i')
                msg.add_arg(0,arg_type ='i')
                msg.add_arg(0,arg_type ='i')
                msg=msg.build()
                client.send_message('/first',msg)  
                stop_drum1=0
                stop_drum2=1
                stop_seq1=0
                stop_seq2=0
                stop_seq3=0
                
                
                
    im2, contours, hierarchy = cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)        
    for pic,contour in enumerate(contours):
        area=cv2.contourArea(contour)
        if (area>300):
            x,y,w,h=cv2.boundingRect(contour)
            img=cv2.rectangle(frame_copy,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img,"",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,255,0))
            
            if (x>x_bass_min)and(x<x_bass_max)and(y>y_bass_min)and(y<y_bass_max)and(stop_seq1==0):
                    
                msg= osc_message_builder.OscMessageBuilder(address="/first")     
                msg.add_arg(100,arg_type ='i')
                msg.add_arg(0,arg_type ='i')
                msg.add_arg(0,arg_type ='i')
                msg=msg.build()
                client.send_message('/first',msg) 
                stop_seq1=1
                stop_seq2=1
                stop_seq3=1
                


            if (x>x_snare_min)and(x<x_snare_max)and(y>y_snare_min)and(y<y_snare_max)and(stop_seq2==0):
                    
                msg= osc_message_builder.OscMessageBuilder(address="/first")     
                msg.add_arg(101,arg_type ='i')
                msg.add_arg(0,arg_type ='i')
                msg.add_arg(0,arg_type ='i')
                msg=msg.build()
                client.send_message('/first',msg)              
                stop_seq2=1
                stop_seq1=1
                stop_seq3=2

    
    
    #-------------- COUNT FINGER FUNCTIONS -------------------  
    
    # Grab the ROI from the frame
    roi = frame[roi_top:roi_bottom, roi_right:roi_left]
    
    if isBgCaptured == 1:
        
        #bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        img = removeBG(roi)
        
        # Apply grayscale and blur to ROI
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        
        ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('ori', thresh)
        
        
        
        # get the coutours
        thresh1 = copy.deepcopy(thresh)
        _,contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1
        if length > 0:
            for i in range(length):  # find the biggest contour (according to area)
                temp = contours[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i

            res = contours[ci]
            hull = cv2.convexHull(res)
            drawing = np.zeros(img.shape, np.uint8)
            cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            isFinishCal,cnt = calculateFingers(res,drawing)
            
            finger_val=isFinishCal

            if isFinishCal is True and cnt <=1:
                
                #cv2.putText(frame_copy, str(cnt+1), (60, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 3)
                count=cnt
                
                if (cnt==0)and(stop1==0):
                    msg = osc_message_builder.OscMessageBuilder(address="/first")     
                    msg.add_arg(400,arg_type ='i')
                    msg.add_arg(x_pos_yellow,arg_type ='i')
                    msg.add_arg(y_pos_yellow,arg_type ='i')  
                    msg=msg.build()
                    client.send_message('/first',msg)
                    
                    stop1=1
                    stop2=0
                    stop3=0
                    
                    
                if (cnt==1)and(stop2==0):
                    msg = osc_message_builder.OscMessageBuilder(address="/first")     
                    msg.add_arg(600,arg_type ='i')
                    msg.add_arg(x_pos_yellow,arg_type ='i')  
                    msg.add_arg(y_pos_yellow,arg_type ='i')  
                    msg=msg.build()
                    client.send_message('/first',msg)
                    stop2=1
                    stop1=0
                    stop3=0
                    
                             
        cv2.imshow('output', drawing)
        
        
        
        
    #  ILLIMUNATION FINGER DRAWING FUNCTION 
    
    if (count==0) and (stop_count1==0) :
        stop_count1=1
        stop_count2=0      
        cv2.rectangle(blend2, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), -1)
        cv2.addWeighted(blend2, 0.5, frame_copy, 1 - 0.5, 0, frame_copy)
              
    if (count==1) and (stop_count2==0) :
        stop_count1=0
        stop_count2=1   
        cv2.rectangle(blend2, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), -1)
        cv2.addWeighted(blend2, 0.5, frame_copy, 1 - 0.5, 0, frame_copy)
    
    
    #  ILLIMUNATION NOTE DRAWING FUNCTION 
      
    if (x_pos_yellow>325)and(x_pos_yellow<450)and(y_pos_yellow>10)and(y_pos_yellow<125):
        cv2.rectangle(blend2,(327,12),(448,123),(0,0,255),-1)  
        cv2.addWeighted(blend2, 0.5, frame_copy, 1 - 0.5, 0, frame_copy)
     
     
    if (x_pos_yellow>451)and(x_pos_yellow<575)and(y_pos_yellow>10)and(y_pos_yellow<125):
        cv2.rectangle(blend2,(452,12),(573,123),(0,0,255),-1) 
        cv2.addWeighted(blend2, 0.5, frame_copy, 1 - 0.5, 0, frame_copy)
    
    
    if (x_pos_yellow>326)and(x_pos_yellow<450)and(y_pos_yellow>126)and(y_pos_yellow<240):
        cv2.rectangle(blend2,(328,128),(448,238),(0,0,255),-1)    
        cv2.addWeighted(blend2, 0.5, frame_copy, 1 - 0.5, 0, frame_copy)
     
    
    if (x_pos_yellow>451)and(x_pos_yellow<575)and(y_pos_yellow>126)and(y_pos_yellow<240):
        cv2.rectangle(blend2,(452,128),(573,238),(0,0,255),-1)  
        cv2.addWeighted(blend2, 0.5, frame_copy, 1 - 0.5, 0, frame_copy)
        
        
    #  ILLIMUNATION DRUM DRAWING FUNCTION 
    
    if (stop_drum1==1):
        cv2.rectangle(blend2,(x_bass_min,y_bass_min),(x_bass_max,y_bass_max),(0,255,0),-1)
        cv2.addWeighted(blend2, 0.4, frame_copy, 1 - 0.4, 0, frame_copy)
        
    if (stop_drum2==1):
        cv2.rectangle(blend2,(x_snare_min,y_snare_min),(x_snare_max,y_snare_max),(0,255,0),-1)  
        cv2.addWeighted(blend2, 0.4, frame_copy, 1 - 0.4, 0, frame_copy)
        
        
        
        
    #  ILLIMUNATION SYNTH DRAWING FUNCTION 
    
    if (stop_seq3==1):
        cv2.rectangle(blend2,(x_bass_min+20,y_bass_min+20),(x_bass_max-20,y_bass_max-20),(255,0,0),-1)
        cv2.addWeighted(blend2, 0.4, frame_copy, 1 - 0.4, 0, frame_copy)
        
    if (stop_seq3==2):
        cv2.rectangle(blend2,(x_snare_min+20,y_snare_min+20),(x_snare_max-20,y_snare_max-20),(255,0,0),-1)  
        cv2.addWeighted(blend2, 0.4, frame_copy, 1 - 0.4, 0, frame_copy)
        

    # NOTE DRAWING FUNCTION 
    
    cv2.rectangle(frame_copy,(325,10),(450,125),(255,0,0),2)
    cv2.rectangle(frame_copy,(451,10),(575,125),(255,0,0),2)
    cv2.rectangle(frame_copy,(325,126),(450,240),(255,0,0),2)
    cv2.rectangle(frame_copy,(450,126),(575,240),(255,0,0),2)
    
    cv2.putText(frame_copy,"C",(325+30,10+60),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),3) 
    cv2.putText(frame_copy,"C#",(451+30,10+60),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),3)  
    cv2.putText(frame_copy,"E",(326+30,126+60),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),3)
    cv2.putText(frame_copy,"F",(450+30,126+60),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),3)
    
    
    # DRUM DRAWING FUNCTION 
    
    img=cv2.rectangle(frame_copy,(x_bass_min,y_bass_min),(x_bass_max,y_bass_max),(255,0,0),2)
    img=cv2.rectangle(frame_copy,(x_snare_min,y_snare_min),(x_snare_max,y_snare_max),(255,0,0),2)    
            
    cv2.putText(frame_copy,"4/4",(x_bass_min+30,y_bass_min+50),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),3)
    cv2.putText(frame_copy,"6/8",(x_snare_min+30,y_snare_min+50),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),3)
    
    
    # FINGER DRAWING FUNCTION 
      
    if finger_val is True:
        cv2.putText(frame_copy, str(count+1), (60, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 3)

    
    # ROI DRAWING FUNCTION 
 
    cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), 5)
    
    # USER HELPFUL GUIDE
    
    cv2.putText(frame_copy,"Press 'b' to capture background ",(10,440),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1)
    cv2.putText(frame_copy,"Press 'r' and 'b' to reset and recapture background ",(10,465),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1)
    cv2.putText(frame_copy,"Press 'q' to stop sound",(10,415),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1)
    cv2.putText(frame_copy,"Press 'esc' to exit ",(10,390),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1)
    
    
    

    
    cv2.imshow("Finger Count", frame_copy)
        
        
        
    # Keyboard OP
    if cv2.waitKey(25) & 0xFF == ord('q'): 
        msg = osc_message_builder.OscMessageBuilder(address="/first")     
        msg.add_arg(200,arg_type ='i')
        msg.add_arg(0,arg_type ='i')
        msg.add_arg(0,arg_type ='i')
        msg=msg.build()
        client.send_message('/first',msg)
        stop_seq1=0
        stop_seq2=0
        stop_seq3=0
        stop_drum1=0
        stop_drum2=0
        img=cv2.rectangle(frame_copy,(x_bass_min,y_bass_min),(x_bass_max,y_bass_max),(255,0,0),2)
        img=cv2.rectangle(frame_copy,(x_snare_min,y_snare_min),(x_snare_max,y_snare_max),(255,0,0),2)  
        
    
    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        msg = osc_message_builder.OscMessageBuilder(address="/first")     
        msg.add_arg(200,arg_type ='i')
        msg.add_arg(0,arg_type ='i')
        msg.add_arg(0,arg_type ='i')
        msg=msg.build()
        client.send_message('/first',msg)
        break
    elif k == ord('b'):  # press 'b' to capture the background
        bgModel = cv2.createBackgroundSubtractorMOG2(10, bgSubThreshold)
        isBgCaptured = 1
        print( '!!!Background Captured!!!')
    elif k == ord('r'):  # press 'r' to reset the background
        bgModel = None
        triggerSwitch = False
        isBgCaptured = 0
        print ('!!!Reset BackGround!!!')

        
        
# Release the camera and destroy all the windows
cam.release()
cv2.destroyAllWindows()