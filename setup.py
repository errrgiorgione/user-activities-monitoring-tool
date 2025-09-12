import os

path = r".\activities"

try: os.mkdir(path)
except FileExistsError: print("Folder already exists")
except Exception as e: print("An error occurred: ", e)

week_days = [0, 1, 2, 3, 4, 5, 6] #0 = monday, 6 = sunday

try:
    for day in week_days:
        file_path = f"{path}\\activities_{day}.json"
        if not os.path.isfile(file_path):
            with open(file_path, "w") as file:
                pass
except:
    print("An error occured. The setup may not be complete")
