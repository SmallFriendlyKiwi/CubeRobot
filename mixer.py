import cube_robot as cr

# scramble = input("Enter cube scramble: ")
scramble = "R' U B' D L2 R F2 U' L U' L R' F L U' D2 R2 L D B2 U' R L D' R2"

scramble_list = scramble.split()

for notation in scramble_list:
    print(notation)

exit()

# set_servo_speeds(speed_unrestricted)
cr.set_servo_speeds(cr.servo_speed)

cr.initialise()

print("Mixing...")
cr.go("f")
cr.go("u")
cr.go("f")
cr.go("u")
cr.go("r")
cr.go("u")
cr.go("r")
cr.go("u")
cr.go("r")
cr.go("b")

print("Solving...")
cr.go("b_inv")
cr.go("r_inv")
cr.go("u_inv")
cr.go("r_inv")
cr.go("u_inv")
cr.go("r_inv")
cr.go("u_inv")
cr.go("f_inv")
cr.go("u_inv")
cr.go("f_inv")

cr.sliders_backwards()
    
# for x in range(3400, 6300, 50):
#     print(x)
#     servo.setTarget(slider_d, x)
#     sleep(0.2)