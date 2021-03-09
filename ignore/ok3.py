import json

with open("schedule1.json", "r") as f:
    sch = json.load(f)

new = {}

for group in sch.keys():
    print(group)
    daydata = {}
    routine = sch[group]
    day = "SUN"
    for classdata in routine:
        if day not in daydata.keys(): daydata[day] = []
        if day == classdata['Day']: daydata[day].append(classdata)
        day = classdata['Day']
    new[group] = daydata

with open("new.json", "w") as f:
    json.dump(new, f, indent = 4)