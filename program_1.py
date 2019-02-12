from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from tqdm import tqdm
from config import *
from shutil import copyfile


def urlfix(urlarr):
    fixedurls = []
    for url_ in urlarr:
        spliturl = url_.split("?")[0]
        if spliturl[-4:] == ".php":  # https://www.facebook.com/profile.php?id=xxxblabla
            firstpart = url_.split("&")[0]
            secondpart = "&%2Ffriends&sk=friends&source_ref=pb_friends_tl"
        else:  # https://www.facebook.com/xxx?fref=pb&hc_location=friends_tab
            firstpart = spliturl
            secondpart = "/friends"
        fixedurl = firstpart + secondpart
        fixedurls.append(fixedurl)
    return fixedurls


def remove_deleted_accounts(namearr, urlarr):
    mergedarr = []
    counter = 0
    for ii in range(len(namearr)):
        if config_url not in urlarr[ii]:  # The removed profile links to your own friend list.
            mergedarr.append("{0} - {1}\n".format(namearr[ii], urlarr[ii]))
        else:
            counter += 1
            mergedarr.append("{0} - Account deleted\n".format(namearr[ii]))
    print("Detected {0} deleted accounts.".format(counter))
    return mergedarr


def getfriendcount():
    # Frist attempt, most occuring div:
    divcontent = [post.text for post in driver.find_elements_by_xpath("//div[contains(@class,'_3dc lfloat _ohe _5brz _5bry')]/a")]
    if len(divcontent) != 0:  # divcontent is empty if this div is not on the page.
        friendstring = divcontent[0]
        friendcount = ''
        for i in friendstring:
            if i in "1234567890":
                friendcount = friendcount + i
    else:
        # Second attempt, other kind of div, for some reason.
        divcontent = [post.text for post in driver.find_elements_by_xpath("//div[contains(@class,'_3dc lfloat _ohe _5brz')]/a")]
        friendstring = divcontent[0]
        friendcount = ''
        for i in friendstring:
            if i in "1234567890":
                friendcount = friendcount + i

    return int(friendcount)


def scrollcalc(friendcnt):
    amount_of_lines = int(friendcnt / 2)
    amount_of_pixels = amount_of_lines * 113
    amount_of_scrolls = int(amount_of_pixels / 400) + 1
    return amount_of_scrolls


# Check config, exit if we are missing flags.
if config_url != '' or config_name != '' or config_password != '' or config_email != '':
    print("Running scraper for {0} ({1})".format(config_name, config_email))
else:
    print("Error: one or more of the options in the config file is empty!\nTerminating...")
    exit()

# Check if this script has already ran.
try:
    with open("friends.dat", "r") as file:
        print("Warning: friends.dat already exists, which means you have already run this script."
              " Running it again will overwrite the old file.")
    while True:
        response = input("Do you want to continume? (Y/n) # ")
        if response.lower() == "y":
            break
        elif response.lower() == "n":
            print("Terminating...")
            exit()
        else:
            continue
except IOError:
    pass

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
driver.get(config_url)

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

# Get urls and change them into friend list urls
urlspre = driver.find_elements_by_xpath("//div[contains(@class,'fsl fwb fcb')]/a")
urls = []
for elem in urlspre:
    urls.append(elem.get_attribute('href'))
friend_urls = urlfix(urls)

# Get list with all names combined with URLs, detect deleted accounts.
friend_master = remove_deleted_accounts(friend_names, friend_urls)

# Print friend list in CLI
for entry in friend_master:
    print(entry[:-1])  # Not to include the newline character at the end.

# Make master user's friendlist file
print("Saving friend list...")
with open("{0}.list".format(config_name), "w") as file:
    for name in friend_names:
        file.write("{0}\n".format(name))

# Make master link list
print("Saving datafile...")
with open("friends.dat", "w") as file:
    for entry in friend_master:
        if "Account deleted" not in entry:  # Leave deleted accounts out of the datafile.
            file.write(entry)


copyfile("friends.dat", "friends.dat.bak")

print("Done! Exiting...")
