# fb_scraper

Facebook friend scraper, gets you a list of all your friends, and all their friends.

Works with Python3. (I used 3.7, I have no idea if this works in older versions of Pytyhon3, Python2 will NOT work.)

Instructions:

Install the requirements with pip:
$ sudo pip3 install -r ./requirements.txt

Install Firefox. (You could also modify the script to use Chrome instead, but I have not tested this.)

On GNU/Linux, Selenium is able to automatically detect the location of the geckodriver, which means the script will work. On Windows, and perhaps on Mac as well (have not tested), it does not and you need to specify it in the python script. Google is your friend. (You might 
also need to do this if it does not get detected automatically in GNU/linux.

Enter the correct information in the config.py file. Make sure to type the values between ''.

Run program_1.py, This will create a list of your own friends, as well as a datafile that contains all your friends' names with links to their friend pages. This datafile is required by the second program. A backup of this file is also made.

Run program_2.py, this will create lists of your friends' friends, scraping their friend pages one by one. This will take a while. When a friend is processed, they are removed from the datafile, which means that you can always stop this script and it will continue where it 
left off when you run it again.

All friend lists are saved as Name.list, the datafile is friends.dat (backup is friends.dat.bak).

I am not a professional programmer, so don't expect too much fancyness from this. If you have improvements, feel free to open a PR or fork it.
