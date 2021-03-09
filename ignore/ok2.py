import json

with open('schedule.json', 'r') as f:
    schedule = json.load(f)

y = []


for x in schedule['C5']:
    if x['Class Type'] == "Lecture" or x['Class Type'] == "Workshop":print(x['Lecturer'], x['Module Title '])
#     y.append(x['Lecturer'])

# z = set(y)

# for a in z:
#     print(a)
# print(len(z))