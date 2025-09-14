from datetime import datetime as dt
import json
from os import path

column1 = "Process"
column2 = "Running time (hours)"

days = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday"
}

while True:
    try:

        day = input("Leave blank to show today's activities or specify the number of the day you want to be shown (0 = monday, 6 = sunday): ")
        if not day: 
            day = dt.today().weekday()
            json_file_path = fr"./activities/activities_{day}.json"
        elif day and day.isnumeric(): 
            day = int(day)
            if day >= 0 and day <= 6: json_file_path = fr"./activities/activities_{day}.json"
            else: continue
        else: continue

        if path.getsize(json_file_path) == 0:
            print(f"No data found for last {days[int(day)]}")
            continue
        
        print(f"{column1:<30}\t| {column2:<30}\t| State")
        print("-"*100)
        with open(json_file_path, "r") as file:
            content = json.load(file)

        processes = list(content.keys())
        for process in processes:
            temp = content[process]["running_time"]
            
            time = temp if temp else (dt.strptime(dt.now().strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S") - dt.strptime(content[process]["start_time"], "%d/%m/%Y %H:%M:%S")).total_seconds()
            time = round(time / 60 / 60, 2)
            same_day = True if dt.today().weekday() == day else False

            if temp: status = "Ended"
            else:
                if same_day: status = "Still running"
                else: status = f"Didn't end on {days[int(day)]}"

            print(f"{process:<30}\t| {time:<30}\t| {status}")
    except Exception as e:
        print(e)