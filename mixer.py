import cube_robot as cr

# scramble = input("Enter cube scramble: ")
# scramble = "R' U B' D L2 R F2 U' L U' L R' F L U' D2 R2 L D B2 U' R L D' R2"
scramble = "B2 R' B2 U L2 B D' U2 F R2"

scramble_list = scramble.split()

cr.set_servo_speeds(cr.servo_speed)
cr.initialise()

print("Scrambling Cube...")
for step in scramble_list:
    print("Currently processing step: " + step)
    step = cr.notation_dictionary[step]
    cr.go(step)

print("Solving Cube...")
for step in reversed(scramble_list):
    step = cr.inverse_notation_dictionary[step]
    cr.go(step)

print("Solved!!!")
cr.sliders_backwards()

exit()