#!/usr/bin/env python3
import re
import sys

if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' <gcode file> <height>')
    sys.exit(1)

with open(sys.argv[1],"r") as gcode_file:
    gcode : str = gcode_file.read()
height : float = float(sys.argv[2])

gcode = gcode.splitlines()
moves = [x for x in gcode if ("G1" or "G2" or "G0") in x][:-4]
moves = [re.sub(r"G.","G2",x) for x in moves]
moves = [re.sub(r" E-?\d+\.?\d*","",x) for x in moves]
moves = [re.sub(r"Z(-?\d+\.?\d*)", lambda x: "Z"+str(height-float(x.group(1))),y) for y in moves]
moves = [re.sub(r" F-?\d+\.?\d*","",x) for x in moves]
#moves = [x.strip() for x in moves]
print("""
M413 S0 ; Disable power loss recovery
M107 ; Fan off
M104 S0 ; Set target temperature
G92 E0 ; Hotend reset

G90 ; Absolute positioning

G28 X Y ; Home X and Y axes

G0 X80 Y80 F5000.0 ; Move to start position

G91 ; Relative positioning
G0 Z-20 ; move down
G90 ; Absolute positioning


; START OF PRINT

M204 S2000 ; Printing and travel speed in mm/s/s

""")

print(str(moves).replace(',','\n').replace("'","").replace(" G2","G2").strip("[]"))

print("""
; END OF PRINT

G91 ; Relative positioning
G0 Z40 ; Raise Z more

G90 ; Absolute positioning
G0 X0 Y220 ; Present print

M84 X Y E ; Disable all steppers but Z
M84 Z
""")
# finishedGcode:str = ""
# for opcode in gcode:
#     finishedGcode+=opcode+'\n'
# print(finishedGcode)