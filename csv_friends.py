from os import listdir
from config import *


def getnamelist():
    namelist = ["nothing", config_name]
    with open("{0}.list".format(config_name), "r") as file4:
        for line2 in file4:
            namelist.append(line2[:-1])
    return namelist


def getfilelist():
    filelist = listdir()
    fixedfilelist = []
    for file3 in filelist:
        if ".list" in file3:
            fixedfilelist.append(file3)
    return fixedfilelist


# Get file list and make the array of all people
file_list = getfilelist()
people_list = getnamelist()

# Export first csv file
csv_str_list = []
for (num, name) in enumerate(people_list):
    if num != 0:
        composed = '{0},"{1}"\n'.format(str(num), name)
        csv_str_list.append(composed)

with open("nodes.csv", "w") as file:
    file.write("ID,Label\n")
    for composedstr in csv_str_list:
        file.write(composedstr)
print("csv exported!")

# Put all people in a dictionary
people_dict = {}
for i in range(len(people_list)):
    people_dict[people_list[i]] = i

# Save edges.csv
with open("edges.csv", "w") as edges:
    edges.write("Source,Target\n")
    for filename in file_list:
        master_name = filename[:-5]
        master_int = people_dict[master_name]
        with open(filename, "r") as file:
            file_lines = file.readlines()
            for line in file_lines:
                slave_name = line[:-1]  # Split off \n
                if slave_name in people_list:
                    slave_int = people_dict[slave_name]
                    edges.write("{0},{1}\n".format(str(master_int), str(slave_int)))
        print("{0} Done!".format(filename))
