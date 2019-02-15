from os import listdir
from config import *
from tqdm import tqdm


def addtoarr(masterarr, filename):  # Creates array with the names of all the people.
    with open(filename, "r") as file2:
        for line2 in file2:  # I suck at naming variables, I don't give a shit.
            name2 = line2[:-1]  # remove \n
            if name2 not in masterarr:
                masterarr.append(name2)
    return masterarr


def getfilelist():  # Gets a list of all .list files. (Files that contain friend information)
    filelist = listdir()
    fixedfilelist = []
    for file3 in filelist:
        if ".list" in file3:
            fixedfilelist.append(file3)
    return fixedfilelist


# Get file list and make the array of all people
file_list = getfilelist()
people_list = ["nothing", config_name]

print("Processing listfiles, this can take a while...")
for file in tqdm(file_list):
    addtoarr(people_list, file)
print("All listfiles processsed!")

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
        master_int = people_dict[master_name]  # Gets the integer belonging to that name, needed for the csv
        with open(filename, "r") as file:
            file_lines = file.readlines()
            for line in file_lines:
                slave_name = line[:-1]  # Split off \n
                slave_int = people_dict[slave_name]
                edges.write("{0},{1}\n".format(str(master_int), str(slave_int)))
print("edges.csv exported!")
