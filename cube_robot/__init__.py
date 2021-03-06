from typing import List
import maestro
from time import sleep

# Configure gripper servo channels
gripper_r = 0
gripper_l = 6
gripper_u = 2
gripper_d = 8

# Configure slider channels
slider_r = 1
slider_l = 7
slider_u = 3
slider_d = 9

notation_dictionary = {
    "F": "F",
    "R": "R",
    "U": "U",
    "B": "B",
    "L": "L",
    "D": "D",
    "F'": "F_INV",
    "R'": "R_INV",
    "U'": "U_INV",
    "B'": "B_INV",
    "L'": "L_INV",
    "D'": "D_INV",
    "F2": "F2",
    "R2": "R2",
    "U2": "U2",
    "B2": "B2",
    "L2": "L2",
    "D2": "D2"
}

inverse_notation_dictionary = {
    "F": "F_INV",
    "R": "R_INV",
    "U": "U_INV",
    "B": "B_INV",
    "L": "L_INV",
    "D": "D_INV",
    "F'": "F",
    "R'": "R",
    "U'": "U",
    "B'": "B",
    "L'": "L",
    "D'": "D",
    "F2": "F2",
    "R2": "R2",
    "U2": "U2",
    "B2": "B2",
    "L2": "L2",
    "D2": "D2"
}

colour_to_face_dictionary = {
    "W": "U",
    "G": "F",
    "O": "L",
    "R": "R",
    "B": "B",
    "Y": "D"
}

# Speed combinations that work well: 0.4 / 80
speed_unrestricted = 0
time_between_actions = .4
servo_speed = speed_unrestricted

# Configure gripper 0 Degree and 90 Degree targets
gripper_r_0 = 3000
gripper_r_90 = gripper_r_0 + 2550

gripper_l_0 = 3600
gripper_l_90 = gripper_l_0 + 2550

gripper_u_0 = 5400
gripper_u_90 = gripper_u_0 + 2550

gripper_d_0 = 3650
gripper_d_90 = gripper_d_0 + 2550

# Configure slider targets:
# b = back
# f = forwards

slider_d_b = 3400
slider_d_f = slider_d_b + 3100

slider_u_b = 3500
slider_u_f = slider_u_b + 3100

slider_r_b = 3200
slider_r_f = slider_r_b + 3250

slider_l_b = 2900
slider_l_f = slider_l_b + 3250

#
# Face layour for kociemba algorithm
#
#              |************|
#              |*U1**U2**U3*|
#              |************|
#              |*U4**U5**U6*|
#              |************|
#              |*U7**U8**U9*|
#              |************|
#  ************|************|************|************
#  *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*
#  ************|************|************|************
#  *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
#  ************|************|************|************
#  *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
#  ************|************|************|************
#              |************|
#              |*D1**D2**D3*|
#              |************|
#              |*D4**D5**D6*|
#              |************|
#              |*D7**D8**D9*|
#              |************|
#
# A cube definition string "UBL..." means that in position U1 we have the U-color,
# in position U2 we have the B-color, in position U3 we have the L color etc. according
# to the order U1, U2, U3, U4, U5, U6, U7, U8, U9, R1, R2, R3, R4, R5, R6, R7, R8, R9, 
# F1, F2, F3, F4, F5, F6, F7, F8, F9, D1, D2, D3, D4, D5, D6, D7, D8, D9, L1, L2, L3, 
# L4, L5, L6, L7, L8, L9, B1, B2, B3, B4, B5, B6, B7, B8, B9.

# Face layout for colour ensuring that Green is F and white is U
#
#              |************|
#              |*W1**W2**W3*|
#              |************|
#              |*W4**W5**W6*|
#              |************|
#              |*W7**W8**W9*|
#              |************|
#  ************|************|************|************
#  *O1**O2**O3*|*G1**G2**G3*|*R1**R2**R3*|*B1**B2**B3*
#  ************|************|************|************
#  *O4**O5**O6*|*G4**G5**G6*|*R4**R5**R6*|*B4**B5**B6*
#  ************|************|************|************
#  *O7**O8**O9*|*G7**G8**G9*|*R7**R8**R9*|*B7**B8**B9*
#  ************|************|************|************
#              |************|
#              |*Y1**Y2**Y3*|
#              |************|
#              |*Y4**Y5**Y6*|
#              |************|
#              |*Y7**Y8**Y9*|
#              |************|
# 
# A cube definition string "GYO..." means that in position W1 we have the G-color,
# in position W2 we have the Y-color, in position W3 we have the O color etc. according
# to the order W1, W2, W3, W4, W5, W6, W7, W8, W9, R1, R2, R3, R4, R5, R6, R7, R8, R9, 
# G1, G2, G3, G4, G5, G6, G7, G8, G9, Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8, Y9, O1, O2, O3, 
# O4, O5, O6, O7, O8, O9, B1, B2, B3, B4, B5, B6, B7, B8, B9.
#
# Where:
#
# W = White
# R = Red
# G = Green
# Y = Yellow
# O = Orange
# B = Blue
#

servo = maestro.Controller()

def colour_to_face(definition_string: str):
    result = ""
    for colour in definition_string:
        face = colour_to_face_dictionary[colour]
        result += face
    return result
    

def sliders_forwards():
    servo.setTarget(slider_l, slider_l_f)
    servo.setTarget(slider_r, slider_r_f)
    servo.setTarget(slider_u, slider_u_f)
    servo.setTarget(slider_d, slider_d_f)
    sleep(time_between_actions)
    
def sliders_backwards():
    servo.setTarget(slider_l, slider_l_b)
    servo.setTarget(slider_r, slider_r_b)
    servo.setTarget(slider_u, slider_u_b)
    servo.setTarget(slider_d, slider_d_b)

def grippers_0():
    servo.setTarget(gripper_l, gripper_l_0)
    servo.setTarget(gripper_r, gripper_r_0)
    servo.setTarget(gripper_u, gripper_u_0)
    servo.setTarget(gripper_d, gripper_d_0)

def grippers_90():
    servo.setTarget(gripper_l, gripper_l_90)
    servo.setTarget(gripper_r, gripper_r_90)
    servo.setTarget(gripper_u, gripper_u_90)
    servo.setTarget(gripper_d, gripper_d_90)

def set_servo_speeds(speed: int):
    servo.setSpeed(gripper_l,speed)
    servo.setSpeed(gripper_r, speed)
    servo.setSpeed(gripper_u, speed)
    servo.setSpeed(gripper_d, speed)

    servo.setSpeed(slider_l, speed)
    servo.setSpeed(slider_r, speed)
    servo.setSpeed(slider_u, speed)
    servo.setSpeed(slider_d, speed)

def initialise(load_time: int):
    sliders_backwards()
    sleep(time_between_actions)
    grippers_0()
    sleep(load_time)
    sliders_forwards()

def go(action: str):
    if action == "R":
        rotate_clockwise(gripper_r, slider_r, gripper_r_0, gripper_r_90, slider_r_f, slider_r_b)
    
    elif action == "L":
        rotate_clockwise(gripper_l, slider_l, gripper_l_0, gripper_l_90, slider_l_f, slider_l_b)
    
    elif action == "U":
        rotate_clockwise(gripper_u, slider_u, gripper_u_0, gripper_u_90, slider_u_f, slider_u_b)
    
    elif action == "D":
        rotate_clockwise(gripper_d, slider_d, gripper_d_0, gripper_d_90, slider_d_f, slider_d_b)
    
    elif action == "F":
        set_front_back()
        rotate_clockwise(gripper_r, slider_r, gripper_r_0, gripper_r_90, slider_r_f, slider_r_b)
        reset_front_back()
    
    elif action == "B":
        set_front_back()
        rotate_clockwise(gripper_l, slider_l, gripper_l_0, gripper_l_90, slider_l_f, slider_l_b)
        reset_front_back()
    
    elif action == "R_INV":
        rotate_anticlockwise(gripper_r, slider_r, gripper_r_0, gripper_r_90, slider_r_f, slider_r_b)
    
    elif action == "L_INV":
        rotate_anticlockwise(gripper_l, slider_l, gripper_l_0, gripper_l_90, slider_l_f, slider_l_b)
    
    elif action == "U_INV":
        rotate_anticlockwise(gripper_u, slider_u, gripper_u_0, gripper_u_90, slider_u_f, slider_u_b)
    
    elif action == "D_INV":
        rotate_anticlockwise(gripper_d, slider_d, gripper_d_0, gripper_d_90, slider_d_f, slider_d_b)
    
    elif action == "F_INV":
        set_front_back()
        rotate_anticlockwise(gripper_r, slider_r, gripper_r_0, gripper_r_90, slider_r_f, slider_r_b)
        reset_front_back()
    
    elif action == "B_INV":
        set_front_back()
        rotate_anticlockwise(gripper_l, slider_l, gripper_l_0, gripper_l_90, slider_l_f, slider_l_b)
        reset_front_back()

    elif action == "R2":
        go("R")
        go("R")
    
    elif action == "L2":
        go("L")
        go("L")
    
    elif action == "U2":
        go("U")
        go("U")
    
    elif action == "D2":
        go("D")
        go("D")
    
    elif action == "F2":
        set_front_back()
        rotate_clockwise(gripper_r, slider_r, gripper_r_0, gripper_r_90, slider_r_f, slider_r_b)
        rotate_clockwise(gripper_r, slider_r, gripper_r_0, gripper_r_90, slider_r_f, slider_r_b)
        reset_front_back()
    
    elif action == "B2":
        set_front_back()
        rotate_clockwise(gripper_l, slider_l, gripper_l_0, gripper_l_90, slider_l_f, slider_l_b)
        rotate_clockwise(gripper_l, slider_l, gripper_l_0, gripper_l_90, slider_l_f, slider_l_b)
        reset_front_back()
    
def rotate_clockwise(gripper: int, slider: int, gripper_0: int, gripper_90: int, slider_f: int, slider_b: int):
    servo.setTarget(gripper,gripper_90)
    sleep(time_between_actions)
    servo.setTarget(slider, slider_b)
    sleep(time_between_actions)
    servo.setTarget(gripper,gripper_0)
    sleep(time_between_actions)
    servo.setTarget(slider, slider_f)
    sleep(time_between_actions)

def rotate_anticlockwise(gripper: int, slider: int, gripper_0: int, gripper_90: int, slider_f: int, slider_b: int):
    servo.setTarget(slider, slider_b)
    sleep(time_between_actions)
    servo.setTarget(gripper,gripper_90)
    sleep(time_between_actions)
    servo.setTarget(slider, slider_f)
    sleep(time_between_actions)
    servo.setTarget(gripper,gripper_0)
    sleep(time_between_actions)

def set_front_back():
    servo.setTarget(slider_u, slider_u_b)
    sleep(time_between_actions)
    servo.setTarget(gripper_u, gripper_u_90)
    sleep(time_between_actions)
    servo.setTarget(slider_u, slider_u_f)
    sleep(time_between_actions)
    servo.setTarget(slider_r, slider_r_b)
    servo.setTarget(slider_l, slider_l_b)
    sleep(time_between_actions)
    servo.setTarget(gripper_u, gripper_u_0)
    servo.setTarget(gripper_d, gripper_d_90)
    sleep(time_between_actions)
    servo.setTarget(slider_r, slider_r_f)
    servo.setTarget(slider_l, slider_l_f)
    sleep(time_between_actions)
    servo.setTarget(slider_d, slider_d_b)
    sleep(time_between_actions)
    servo.setTarget(gripper_u, gripper_u_0)
    servo.setTarget(gripper_d, gripper_d_0)
    sleep(time_between_actions)
    servo.setTarget(slider_d, slider_d_f)
    sleep(time_between_actions)

def reset_front_back():
    servo.setTarget(slider_d, slider_d_b)
    sleep(time_between_actions)
    servo.setTarget(gripper_d, gripper_d_90)
    sleep(time_between_actions)
    servo.setTarget(slider_d, slider_d_f)
    sleep(time_between_actions)
    servo.setTarget(slider_r, slider_r_b)
    servo.setTarget(slider_l, slider_l_b)
    sleep(time_between_actions)
    servo.setTarget(gripper_u, gripper_u_90)
    servo.setTarget(gripper_d, gripper_d_0)
    sleep(time_between_actions)
    servo.setTarget(slider_r, slider_r_f)
    servo.setTarget(slider_l, slider_l_f)
    sleep(time_between_actions)
    servo.setTarget(slider_u, slider_u_b)
    sleep(time_between_actions)
    servo.setTarget(gripper_u, gripper_u_0)
    servo.setTarget(gripper_d, gripper_d_0)
    sleep(time_between_actions)
    servo.setTarget(slider_u, slider_u_f)
    sleep(time_between_actions)

def check_scramble(scramble: list):
    try:
        for step in scramble:
            key = notation_dictionary[step]
        return True
    except:
        print("There appears to be an error in the scramble you entered.")
        print("Please try again")
        return False