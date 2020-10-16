# A simple Python + Selenium Bot

This bot is intended to look for availability of GeForce RTX 3080 cards.

It's very straightforward to use but assumes a little knowledge of python.

Tested on Pop!_OS.

## Installation

Installation is reasonable simple.

### Linux

1. Clone the code.
2. Validate that you have Python 3.8 or newer. This code uses newer Python features that are not compatible with Python 3.5
3. Run `sudo apt install firefox-geckodriver; pip3 install selenium`
4. Review the URLs that you would like to monitor in the `rtx_notifier.py` file
5. Run `python3 rtx_notifier.py`

### Windows

1. Clone the code.
2. Install Python 3.8 or newer from the windows store.
3. Download the code and unzip it to a directory
4. Open a PowerShell prompt, navigate into the directory with the source code
5. Execute: `pip3 install selenium`
6. Download GeckoDriver from [https://github.com/mozilla/geckodriver/releases]
7. Unzip the folder and place `geckodriver.exe` into the folder `rtx_notifier`
8. Run the tool using `python3 rtx_notifier.py` using the command prompt.


Please note that this runs multiple, concurrent browsers simultaneously.

If a card is detected as available, the bot will attempt to add the product to your cart and pause all of the other browsers.

Good luck!
