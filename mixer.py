import cube_robot as cr
import kociemba
from time import sleep

initialisation_time = 10
scramble_check: bool = False

print(chr(27) + "[2J")
print("")
print("              |************|")
print("              |*W1**W2**W3*|")
print("              |************|")
print("              |*W4**W5**W6*|")
print("              |************|")
print("              |*W7**W8**W9*|")
print("              |************|")
print("  ************|************|************|************")
print("  *O1**O2**O3*|*G1**G2**G3*|*R1**R2**R3*|*B1**B2**B3*")
print("  ************|************|************|************")
print("  *O4**O5**O6*|*G4**G5**G6*|*R4**R5**R6*|*B4**B5**B6*")
print("  ************|************|************|************")
print("  *O7**O8**O9*|*G7**G8**G9*|*R7**R8**R9*|*B7**B8**B9*")
print("  ************|************|************|************")
print("              |************|")
print("              |*Y1**Y2**Y3*|")
print("              |************|")
print("              |*Y4**Y5**Y6*|")
print("              |************|")
print("              |*Y7**Y8**Y9*|")
print("              |************|")
print("")
print("Orient the cube with green facing the front and white facing up")
print("")
print("A cube definition string 'GYO...' means that in position W1 we have Green,")
print("in position W2 we have Yellow, in position W3 we have Orange etc. according")
print("to the order W1, W2, W3, W4, W5, W6, W7, W8, W9, R1, R2, R3, R4, R5, R6, R7, R8, R9,")
print("G1, G2, G3, G4, G5, G6, G7, G8, G9, Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8, Y9, O1, O2, O3,")
print("O4, O5, O6, O7, O8, O9, B1, B2, B3, B4, B5, B6, B7, B8, B9.")
print("")
print("The face order is: White, Red, Green, Yellow, Orange, Blue")
print("")

cube_definition_string = input("Enter Cube Definition String: ")
cube_definition_string = cube_definition_string.upper()
cube_definition_string = cr.colour_to_face(cube_definition_string)

print("")
print ("Searching for the solution to the Cube Definition String: " + cube_definition_string)
solution_string = kociemba.solve(cube_definition_string)
print("")
print("Solution found: " + solution_string)
print("")
print("Insert your cube ready for solving...")
print("")
print("You have " + str(initialisation_time) + " seconds to insert the cube - mind your fingers...")
print("")
print("Solving the Cube...")
print("")

cr.set_servo_speeds(cr.servo_speed)
cr.initialise(initialisation_time)

move_list = solution_string.split()

for move in move_list:
    print("Processing move: " + move)
    move = cr.notation_dictionary[move]
    cr.go(move)

cr.sliders_backwards()

print("")
print("Solved!!!")
cr.sliders_backwards()

exit()