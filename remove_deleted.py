from config import *


fixedarr = []
counter = 0
with open("friends.dat.bak", "r") as file:
    for line in file:
        if config_url not in line:
            fixedarr.append(line)
        else:
            counter += 1

print("Removed {0} non-existing accounts from your friends list".format(counter))

with open("friends.dat.fixed", "w") as file:
    for line in fixedarr:
        file.write(line)

print("Fixed file saved!")
