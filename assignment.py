## Research Track - Assignment 1 ##
## 	   Jan Drozd (s5646665)      ##
from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the orientation """

d_th = [0.6, 0.4]
""" float: Threshold for the control of the linear distance.
First value for golden tokens, second value for silver ones.
"""

token_record = []
""" Lists of the tokens used in the past"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power += speed
    R.motors[0].m1.power -= speed
    time.sleep(seconds)
#    R.motors[0].m0.power = 0
#    R.motors[0].m1.power = 0

def stop():
    """ Function thats stops the motors """
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token(color):
    """
    Function to find the closest token of the given color

    Arguments:
	color (bool): True if color of the token is silver, False if golden 

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
	token_code (int): stores the token identifier
    """
    dist=100
    for token in R.see():   
        if (token.dist < dist) and (token.info.marker_type is MARKER_TOKEN_SILVER) and (color == True):
            if token.info.offset not in token_record:
                dist = token.dist
                rot_y = token.rot_y
                token_code = token.info.offset
            else:
                continue

        elif (token.dist < dist) and (token.info.marker_type is MARKER_TOKEN_GOLD) and (color == False):
            if token.info.offset not in token_record:
                dist = token.dist
                rot_y = token.rot_y
                token_code = token.info.offset
            else:
                continue
        elif token.dist < dist:
	    continue        

    if dist == 100:
	return -1, -1, -1
    else:
   	return dist, rot_y, token_code

def gripper(token_code, grab):
    """
    Function for grabbing and releasing the tokens
    
    Arguments:
    token_code(int): token identifier
    grab(bool): if True - gipper grabs the token; if False - the token is released
    """
    if grab == True:
        if R.grab():
            stop()
            token_record.append(token_code)
            print("Token grabbed")
        else:
            print("Grabbing unsuccessful")
    else:
        if R.release():
            stop()
            token_record.append(token_code)
            print("Token released")
        else:
            print("Releasing unsuccessful")


def main():
    stop() # initalizes motor speed with 0
    color = True # True if silver, False if golden
    count = 0 # variable counting the turns without seeing any new token of required color
    while len(token_record) < 12: # there are 12 tokens, the loop finishes after handling them all
        dist, rot_y, token_code = find_token(color)
        if dist == -1: # if no token is detected, we make the robot turn 
	        print("I don't see any new token of required color!!")
	        stop()
	        turn(+10, 1)
	        count += 1
	        if count > 8: # if the counter exceeds 8, robot moves forward
	            drive(100, 0.5)
	            count = 0
        elif dist < d_th[color]: # if we are close to the token, we try grab it.
            if color == True:
                #drive(3, 0.5)
                print("Found the silver token!")
                gripper(token_code, color)
                # print(token_record) #debug
            else:
                print("Found the golden token!")
                gripper(token_code, color)
                # print(token_record) #debug
            color = not color # alternates the desired token color
        elif -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	        print("Ah, that'll do.")
	        drive(70, 0.2)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.1)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.1)
    print("Done")

main()
