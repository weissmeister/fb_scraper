from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from tqdm import tqdm
from config import *


def scraper(name, url):
    driver.get(url)
    time.sleep(1)

    # Get friend count and start scrolling
    friendscount = getfriendcount()
    print("Found {0} friends.".format(friendscount))
    scrollcount = scrollcalc(friendscount)

    i = 0
    print("Started scrolling...")
    for scroll in tqdm(range(scrollcount)):
        lo = i * 400
        hi = lo + 400
        driver.execute_script("window.scrollTo({0}, {1});".format(lo, hi))
        sleeptime = 0.25 + random.random() * 0.4
        time.sleep(sleeptime)
        i += 1

    time.sleep(3)
    print("--------------------------------------------------")

    # Get friend names and put them into list
    friend_names = [post.text for post in driver.find_elements_by_xpath("//div[contains(@class,'fsl fwb fcb')]/a")]

    # Print friend list in CLI
    for fname in friend_names:
        print("\t{0}".format(fname))

    # Export the desired file
    print("Saving friends list...")
    with open("{0}.list".format(name), "w") as listfile:
        for fname in friend_names:
            listfile.write("{0}\n".format(fname))


def getfriendcount():
    while True:  # Sometimes this part of the code fails and the div does not get detected randomly.
        # This loop retries on a failed attempt.
        # Frist attempt, most occuring div:
        divcontent = [post.text for post in driver.find_elements_by_xpath("//div[contains(@class,'_3dc lfloat _ohe _5brz _5bry')]/a")]
        if len(divcontent) != 0:
            friendstring = divcontent[0]
            friendcount = ''
            for i in friendstring:
                if i in "1234567890":
                    friendcount = friendcount + i
            return int(friendcount)
        else:
            # Second attempt, other kind of div, for some reason.
            divcontent = [post.text for post in driver.find_elements_by_xpath("//div[contains(@class,'_3dc lfloat _ohe _5brz')]/a")]
            if len(divcontent) !=0:
                friendstring = divcontent[0]
                friendcount = ''
                for i in friendstring:
                    if i in "1234567890":
                        friendcount = friendcount + i
                return int(friendcount)
            print("Warning: Friend count could not be detected. Retrying...")
            time.sleep(5)


def scrollcalc(friendcnt):
    amount_of_lines = int(friendcnt / 2)
    amount_of_pixels = amount_of_lines * 113
    amount_of_scrolls = int(amount_of_pixels / 400) + 1
    return amount_of_scrolls


# Check config and friends.dat, exit if we are missing flags or the file.
if config_url != '' or config_name != '' or config_password != '' or config_email != '':
    print("Config file is set up!")
else:
    print("Error: one or more of the options in the config file is empty!\nTerminating...")
    exit()
try:
    with open("friends.dat", "r") as file:
        print("friends.dat found!")
except IOError:
    print("Error: friends.dat not found, or you have no read permission. Did you run the first program?\nTerminating...")
    exit()


# Open webdriver, log in and load friends page.
print("Starting browser...")
driver = webdriver.Firefox()
driver.get("https://facebook.com")
driver.maximize_window()
assert "Facebook" in driver.title
elem = driver.find_element_by_id("email")
elem.send_keys(config_email)
elem = driver.find_element_by_id("pass")
elem.send_keys(config_password)
elem.send_keys(Keys.RETURN)
time.sleep(5)
print("Logged in...")

while True:  # Main loop, terminates if friends.dat is empty.
    # Read the datafile, determine how many friends we have remaining
    with open("friends.dat", "r") as file:
        file_lines = file.readlines()
    friends_remaining = len(file_lines)

    if friends_remaining == 0:
        print("All friends processed!")
        break
    else:
        print("{0} Friends remaining, processing next entry.".format(friends_remaining))

    # Process data
    splitline = file_lines[0].split(" - ")
    person_name = splitline[0]
    person_url = splitline[1][:-1]  # removing \n
    print("Processing {0}:".format(person_name))
    print("URL = {0}".format(person_url))

    # Call the function and get beer, function does the hard work.
    scraper(person_name, person_url)

    # Delete the processed entry and rewrite the datafile
    print("Removing entry from friends.dat...")
    file_lines.__delitem__(0)
    with open("friends.dat", "w") as file:
        for line_ in file_lines:
            file.write("{0}".format(line_))

    print("{0} processed!".format(person_name))

print("Program complete! Exiting...")
