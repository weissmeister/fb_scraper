from os import listdir
from config import *
from tqdm import tqdm


def getnamelist():  # Gets a list of the names of all the people involved, including config_name.
    namelist = ["nothing", config_name]
    try:
        with open("{0}.list".format(config_name), "r") as file4:
            for line2 in file4:
                namelist.append(line2[:-1])
        return namelist
    except IOError:
        print("Error: {0}.list not found or you do not have read permission.\nTerminating...".format(config_name))
        exit()


def getfilelist():  # Gets a list of all .list files. (Files that contain friend information)
    filelist = listdir()
    fixedfilelist = []
    for file3 in filelist:
        if ".list" in file3:
            fixedfilelist.append(file3)
    return fixedfilelist


# Get file list and make the array of all people
file_list = getfilelist()
people_list = getnamelist()

# Save nodes.csv
with open("nodes.csv", "w") as file:
    file.write("ID,Label\n")
    for (num,name) in enumerate(people_list):
        if num != 0:
            file.write('{0},"{1}"\n'.format(str(num), name))
print("nodes.csv exported!")

# Put all people in a dictionary
people_dict = {}
for i in range(len(people_list)):
    people_dict[people_list[i]] = i

# Save edges.csv
print("Exporting edges.csv...")
with open("edges.csv", "w") as edges:
    edges.write("Source,Target\n")
    for filename in tqdm(file_list):
        master_name = filename[:-5]  # Split off the .list, gives you the full name.
        master_int = people_dict[master_name]  # Gets the integer belonging to that name, needed for the csv.
        with open(filename, "r") as file:  # no IO ex-catching needed since we retrieved the filelist 5 seconds ago.
            file_lines = file.readlines()
            for line in file_lines:
                slave_name = line[:-1]  # Split off \n
                if slave_name in people_list:
                    slave_int = people_dict[slave_name]
                    edges.write("{0},{1}\n".format(str(master_int), str(slave_int)))
print("edges.csv exported!")
