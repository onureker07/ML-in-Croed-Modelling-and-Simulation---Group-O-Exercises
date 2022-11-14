import json

path = input("Enter the scenario path you want to modify: ") #Absolute path or relative path to main project
with open(path,) as f:

    content = json.load(f)

with open(path,"w") as f:
    task = int(input("What do you want to modify\n1- Add pedestrians"))

    if task == 1:
        id = int(input("ID:"))
        x_coor = float(input("X coordinate of the pedestrian"))
        y_coor = float(input("Y coordinate of the pedestrian"))
        target_id =int(input("Target ID:"))
        pedestrian_template = json.load(open("Exercise 2\Templates for Modification\Pedestrian.json"))
        pedestrian_template["attributes"]["id"] = id
        pedestrian_template["position"]["x"] = x_coor
        pedestrian_template["position"]["y"] = y_coor
        pedestrian_template["targetIds"].append(target_id)

        content["scenario"]["topography"]["dynamicElements"].append(pedestrian_template)
        json.dump(content,f,indent=2)
    
