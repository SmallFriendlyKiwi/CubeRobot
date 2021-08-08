import cube_robot as cr
import kociemba
from time import sleep

initialisation_time = 10

scramble_check: bool = False

#cube_definition_string: str = "WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB"
cube_definition_string: str = "BOBGWRGRGYYOORWYBYOBORGGYBOGYBOYWGGBRYWWOWRBRWYWGBORRW"
cube_definition_string = cr.colour_to_face(cube_definition_string)

print ("Searching for the solution to the Cube Definition String: " + cube_definition_string)
# cr.colour_to_face(cube_definition_string)
solution_string = kociemba.solve(cube_definition_string)
print("Solution found: " + solution_string)

exit()

while scramble_check == False:
    scramble = input("Enter cube scramble: ")
    scramble = scramble.upper()
    scramble_list = scramble.split()
    scramble_check = cr.check_scramble(scramble_list)

cr.set_servo_speeds(cr.servo_speed)

# Initialise the robot so that it can
# accept a cube ready for scrambling
# or solving
print("Insert your cube ready for scrambling and solving...")
print("You have " + str(initialisation_time) + " seconds to insert the cube - mind your fingers...")
cr.initialise(initialisation_time)

print("Scrambling the Cube...")
for step in scramble_list:
    print("Processing step: " + step)
    step = cr.notation_dictionary[step]
    cr.go(step)

cr.sliders_backwards()

print("Please wait...")
sleep(5)

cr.sliders_forwards()

print("Solving the cube...")
for step in reversed(scramble_list):
    step = cr.inverse_notation_dictionary[step]
    cr.go(step)

print("Solved!!!")
cr.sliders_backwards()

exit()