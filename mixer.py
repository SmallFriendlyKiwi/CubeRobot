import cube_robot

# scramble = input("Enter cube scramble: ")
scramble = "R' U B' D L2 R F2 U' L U' L R' F L U' D2 R2 L D B2 U' R L D' R2"

scramble_list = scramble.split()

for notation in scramble_list:
    print(notation)

exit()

# set_servo_speeds(speed_unrestricted)
set_servo_speeds(servo_speed)

initialise()

print("Mixing...")
go("f")
go("u")
go("f")
go("u")
go("r")
go("u")
go("r")
go("u")
go("r")
go("b")

print("Solving...")
go("b_inv")
go("r_inv")
go("u_inv")
go("r_inv")
go("u_inv")
go("r_inv")
go("u_inv")
go("f_inv")
go("u_inv")
go("f_inv")

sliders_backwards()
    
# for x in range(3400, 6300, 50):
#     print(x)
#     servo.setTarget(slider_d, x)
#     sleep(0.2)