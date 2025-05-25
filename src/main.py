from fetch import *
import os

data_folder = "/home/burak/Desktop/virtualecon-analysis/data"

if __name__ == "__main__":
    files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))]
    if len(files) >= 100:
        print("Data already fetched.")
    else:
        fetch_items()


