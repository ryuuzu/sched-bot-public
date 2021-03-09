import openpyxl as op
import json

wb = op.load_workbook('timetable.xlsx')
ws = wb['IT Year 1']
schedule = {}
grouplist = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17']
for group in grouplist:
    routine = []
    for row in ws.iter_rows(min_row = 5, max_row = 118):
        groups = row[8].value.split('+')
        # print(type(groups))
        # print(groups)
        if group in groups or "C1-C17" in groups:
            # print("==========================")
            data = {}
            for cell in row:
                titlenot = f'{cell.column_letter}4'
                title = ws[titlenot].value 
                # print(title, ": ", cell.value)
                data[title] = cell.value
            routine.append(data)
        schedule[group] = routine
print(schedule)
with open("schedule1.json", "w") as f:
    json.dump(schedule, f)


# print(dir(cell))
# print(dir(ws))