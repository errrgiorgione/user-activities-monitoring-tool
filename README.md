# About

This Python tool monitors the user's activities, specifically keeping track of the apps the user use and how much time the user spend on every app.
As for when I am writing this README, the tool is still in a testing phase and may fail under certain circumstances.
The data can be shown on CLI using the [user_ui](https://github.com/errrgiorgione/user-activities-monitoring-tool/blob/main/user_ui.py) file.

# How does it work

The tool uses the WMI Python package to access Windows' system informations to find the running process under the user profile. Specifically, the WMI package returns all the running processes on the machine and the tool filters them by their path of origin and their owner.
To filter the processes better the tool uses a list of common and known Windown processes that will not be taken into account during the tracking.

# Usage

To use this tool you first need to run the [setup file](https://github.com/errrgiorgione/user-activities-monitoring-tool/blob/main/setup.py) which will create a folder structured like the one shown below in whatever folder you will run the script.

```
user-activities-monitoring-tool/
┣ activities/
┃ ┣ activities_0.json
┃ ┣ activities_1.json
┃ ┣ activities_2.json
┃ ┣ activities_3.json
┃ ┣ activities_4.json
┃ ┣ activities_5.json
┃ ┗ activities_6.json
┣ main.py
┣ setup.py
┗ windows_processes.txt
```

Each json file will be modified according to the week day (monday = 0, sunday = 6).

### Please keep in mind that the [main file](https://github.com/errrgiorgione/user-activities-monitoring-tool/blob/main/main.py) needs to be located in the same folder as the _activities_ folder and the [windows processes](https://github.com/errrgiorgione/user-activities-monitoring-tool/blob/main/windows_processes.txt) file.

# Other info

To improve the user's experience a few preferences can be set in the [preferences](https://github.com/errrgiorgione/user-activities-monitoring-tool/blob/main/preferences.json) json file. The user can define if to ignore some processes, choose a time unit to use to display the collected data and if to show the extensions of the found processes.

Keep in mind that the only time units available are the following ones and that any other time unit will trigger an error:

- Hours
- Minutes
- Seconds
