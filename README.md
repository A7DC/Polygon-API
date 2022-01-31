# Description

This is the core of the program which takes 5k SYMBOLS and looks back N years to pull in the daily OHLC data of those symbols and saves them to disc.

# Instructions 

1. Download the folder and unzip
2. Open 'Windows terminal'
3. type 'cd' followed by a space and then drag the folder to the terminal window. Press 'enter'
4. type 'pip3 install -r requirements.txt'. Press 'enter'
5. Open 'secrets_EXAMPLE.py' and follow instructions that file
5. type 'python core.py' to run the program. Press 'enter'

# Known issues

1. If we stop the program before it's completed a date, we will have to delete that date manually and start the program again 

# To do

* Add timer to the async function and log it so we know how long each download takes
* Check if there's failed downloads and redownload those dates
* Print to the console so user knows something is happening when program runs

# Resources

I'm not a great programmer so here's where I figured out how to build it:

* [How to download all historic intraday OHCL data from IEX: with Python, asynchronously, via API & for free.](https://towardsdatascience.com/how-to-download-all-historic-intraday-ohcl-data-from-iex-with-python-asynchronously-via-api-b5b04a31b187)
* ['Algorithmic Trading Using Python - Full Course'](https://www.youtube.com/watch?v=xfzGZB4HhEE&t=3143s)



