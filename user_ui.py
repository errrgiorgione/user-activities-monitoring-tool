from datetime import datetime as dt
import json

week_day = dt.today().weekday()
json_file_path = fr"./activities/activities_{week_day}.json"

column1 = "Process"
column2 = "Running time (hours)"
print(f"{column1:<30}\t| {column2:<30}\t| State")
print("-"*100)

try:
    with open(json_file_path, "r") as file:
        content = json.load(file)
    
    processes = list(content.keys())
    for process in processes:
        temp = content[process]["running_time"]

        time = temp if temp else (dt.strptime(dt.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S") - dt.strptime(content[process]["start_time"], "%d/%m/%Y %H:%M:%S")).total_seconds()
        time = round(time / 60 / 60, 2)
        status = "Still running" if not temp else "Ended"

        print(f"{process:<30}\t| {time:<30}\t| {status}")
except Exception as e:
    print(e)