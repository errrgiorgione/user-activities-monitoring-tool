import wmi, getpass, json
from datetime import datetime as dt
from time import sleep
from os import path

user = getpass.getuser()
f = wmi.WMI()
with open("./windows_processes.txt", 'r') as file:
    windows_processes = file.read()
user_folders = [
    r"c:\program files",
    r"c:\program files (x86)",
    fr"c:\users\ktgki\appdata\local\programs",
    fr"c:\users\ktgki\downloads",
    #fr"c:\users\{user.lower()}\appdata\local\programs",
    #fr"c:\users\{user.lower()}\downloads"
]
json_file_path = fr"./activities/activities_{dt.today().weekday()}.json"

running_processes = []
while True:

    user_processes = {}
    if path.getsize(json_file_path) > 0:
        with open(json_file_path, "r") as file:
            listed_processes = json.load(file)
    else: listed_processes = None

    #find and update processes
    start_time = dt.now().strftime("%d/%m/%Y %H:%M:%S")
    processes = f.Win32_Process()
    for process in processes:
        try:
            owner = process.GetOwner()
            name = process.Name
            #short-circuit evaluation
            if name in running_processes or ((user in owner) and (name not in windows_processes) and any(process.ExecutablePath.lower().startswith(folder) for folder in user_folders)):
                for parent in f.Win32_Process(ProcessId=process.ParentProcessId):
                    if parent.Name.lower() != "explorer.exe":
                        continue

                    listed_end_time = listed_processes.get(name, {}).get("end_time", None) if listed_processes else None
                    listed_running_time = listed_processes.get(name, {}).get("running_time", None) if listed_processes else None
                    # if an end_time (or a running_time) was set and the process was found again, then it's a new instance therefore it must be tracked again
                    listed_start_time = listed_processes.get(name, {}).get("start_time", start_time) if listed_processes and not listed_end_time else start_time
                    # if end_time was set and the same process was found again then reset end_time as we are tracking a new istance of the same process now
                    listed_end_time = None if listed_end_time else listed_end_time

                    user_processes[name] = {
                        "start_time": listed_start_time,
                        "end_time": listed_end_time,
                        "running_time": listed_running_time
                    }
                running_processes.append(name)
        except Exception as e: 
            pass
    
    #add end time to processes
    end_time = dt.now().strftime("%d/%m/%Y %H:%M:%S")
    processes_names = [process.Name for process in processes]
    if listed_processes:
        for was_running_process in listed_processes:
            if not was_running_process in processes_names and not listed_processes[was_running_process]["end_time"]:
                listed_start_time = listed_processes[was_running_process]["start_time"]
                listed_running_time = listed_processes[was_running_process].get("running_time", 0)
                if not listed_running_time: listed_running_time = 0 #running_time is set to None by default in the json
                user_processes[was_running_process] = { 
                    "start_time": listed_start_time,
                    "end_time": end_time,
                    "running_time": ((dt.strptime(end_time, "%d/%m/%Y %H:%M:%S") - dt.strptime(listed_start_time, "%d/%m/%Y %H:%M:%S")).total_seconds()) + listed_running_time
                }
    
    #ensure ended processes will still be taken into account
    if listed_processes: 
        for process in listed_processes:
            if process in user_processes.keys() : continue
            user_processes[process] = {
                "start_time": listed_processes[process]["start_time"],
                "end_time": listed_processes[process]["end_time"],
                "running_time": listed_processes[process]["running_time"]
            }

    with open(json_file_path, "w") as file:
        json.dump(user_processes, file)

    sleep(60) 