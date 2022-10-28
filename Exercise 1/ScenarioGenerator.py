file_name = input("File name: ")

open(file_name+".scn", 'w').close() #To clear previous content

with open(file_name+".scn","a") as f:
    f.write(input("Window size: ")+"\n"
    f.write(input("Cell size: ")+"\n")


    nop = int(input("Number of pedestrians: "))
    for i in range(nop):
        f.write(input(str(i+1)+". pedestrian position (format: (x,y)): "))
        if i != nop-1: f.write(" ")
    f.write("\n")

    now = int(input("Number of wall: "))
    for i in range(now):
        is_vertical = True if input("Vertical or Horizontal (type v or h):") == "v" else False
        if is_vertical:
            x = int(input("X position of the wall: "))
            y1 = int(input("Uppermost y position of the wall: "))
            y2 = int(input("Bottom y position of the wall: "))
            for y in range(y1,y2+1):
                f.write("("+str(x)+","+str(y)+") ")

        else:
            y = int(input("Y position of the wall: "))
            x1 = int(input("Rightmost y position of the wall: "))
            x2 = int(input("Leftmost y position of the wall: "))
            for x in range(x1,x2+1):
                f.write("("+str(x)+","+str(y)+") ")
