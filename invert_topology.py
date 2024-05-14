#!/usr/bin/env python3
import re
import sys
deletionList=["M140","M190","M104","M109","G92","M107"]

if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' <gcode file> <height>')
    sys.exit(1)

with open(sys.argv[1],"r") as gcode_file:
    gcode : str = gcode_file.read()
height : float = float(sys.argv[2])
gcode = re.sub(r"E-?\d+\.?\d*","",gcode)
gcode = re.sub(r"Z(-?\d+\.?\d*)", lambda x: "Z"+str(height-float(x.group(1))),gcode)
gcode = re.sub(r"Filament used: .*", "Filament used: 0m", gcode)
gcode = re.sub(r"M117 Printing...", "M117 Embossing...", gcode)

gcode = gcode.splitlines()
finishedGcode:str = ""
for opcode in gcode:
    if opcode.split()[0] not in deletionList:
        finishedGcode+=opcode+'\n'
print(finishedGcode)
