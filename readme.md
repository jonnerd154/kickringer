KickRinger is a Python script for ringing a bell each time a new backer backs a
Kickstarter campaign.  To avoid flooding Kickstarter's servers,
this script periodically retrieves the newest Kickstarter page,
scrapes the data for current backers and dollars pledged,
the randomly distributes bell rings along the update window,
simulating near-realtime performance while being nice to Kickstarter.

INSTALLATION:
    You'll need a couple of Python libraries:
        PySerial: http://pyserial.sourceforge.net/
        BeautifulSoup 4: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
        
    You'll also need a bell or something to ring.  Included with this project is a sample Arduino project
    and a wiring diagram to help you get everything wired up.  This should be really simple.  Here's the BoM:
        1 SparkFun RedBoard or Arduino Uno https://www.sparkfun.com/products/11575
        1 N-Channel MOSFET with high voltage, high current rating AND 1 10K Resistor
            OR
        1 of these MOSFET breakout boards: https://www.sparkfun.com/products/10256
        1 9v >=750mA DC Power Supply https://www.sparkfun.com/products/298
        1 USB Cable for your Arduino/RedBoard
        Miscellaneous hookup wire
        1 Bell w/ solenoid.  There are lots of options here just make sure that your power supply fits the bill.
            I used this: http://www.amazon.com/Thomas-Betts-DH922-Carlon-Doorbell/dp/B000BOJ7UE

    Refer to wiring.pdf for hookup schematics
    
Usage: python kickringer.py <url> <com port> <update interval>

Example: python kickringer.py http://www.kickstarter.com/projects/597507018/pebble-e-paper-watch-for-iphone-and-android 32 10

Credits: This project is built on top of Brad Murray's awesome kickscraper project which served as an excellent
starting point for KickRinger: https://github.com/bradtgmurray/kickscraper

