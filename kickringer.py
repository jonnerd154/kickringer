#
#  kickringer.py
#
#  Created by Jonathan Moyes on 11/3/13.
#  Modular Robotics 2013

#  A Python script for ringing a bell each time a new backer backs a
#  Kickstarter campaign.  To avoid flooding Kickstarter's servers,
#  this script periodically retrieves the newest Kickstarter page,
#  scrapes the data for current backers and dollars pledged,
#  the randomly distributes bell rings along the update window,
#  simulating near-realtime performance while being nice to Kickstarter.
#
#  This project is build on top of the work of Brad Murray's "kickscraper"
#   project https://github.com/bradtgmurray/kickscraper.
#

from bs4 import BeautifulSoup
import urllib2
import sys
import threading
import serial
from random import randint
from time import sleep

def usage():
    sys.stderr.write("kickringer.py <url> <com port> <update interval>\n")

def getBackersAndDollarsWithDifference():
    global url
    global lastBackers
    global lastDollars
    
    # Get the Kickstarter Page
    htmlDoc = urllib2.urlopen(url).read()
    soup = BeautifulSoup(htmlDoc)
    
    # Scrape the data we want
    moneyRaisedDiv = soup.find(id='moneyraised')
    headers = moneyRaisedDiv.find_all('h5')
    backers = headers[0].div.string
    dollars = headers[1].div.data.string
    
    # Remove currency symbol, formatters, convert to float/int
    fDollars = float(dollars[1:].replace(",", ""))
    iBackers = int(backers.replace(",", ""),10)
    
    # Calculate differences in this step
    deltaDollars = fDollars - lastDollars
    deltaBackers = iBackers - lastBackers

    # Update cache variables
    lastDollars = fDollars
    lastBackers = iBackers
    
    return (backers, deltaBackers, dollars, deltaDollars)

def initialize():
    global url;
    global updateInterval;
    global lastDollars
    global lastBackers
    
    url = sys.argv[1]
    updateInterval = int(sys.argv[3])
    lastDollars = 0
    lastBackers = 0
    getBackersAndDollarsWithDifference() # Calling this returns the current data, but also updated the caches.
    initializeSerial()
    pass

def initializeSerial():
    global serialPort
    try:
        serialPort = serial.Serial(int(sys.argv[2])-1) # minus 1 for comport->port conversion
        print "Connection to %s ESTABLISHED" % serialPort.name
    except Exception:
        print "Failed to open connection to serial device on %s.  Exiting." % sys.argv[2]
        sys.exit(1);
    pass

def go():
    global updateInterval

    # Get the newest data
    data = getBackersAndDollarsWithDifference()
    newBackers = data[1]
    
    # Schedule the next update
    threading.Timer(updateInterval, go).start()

    print 'Backers: %s (%s) Dollars: %s (%s)' % data
    
    # If backers have increased, send commands to serial
    if( newBackers > 0):
        global serial_port
        
        print "There are %x new backers" % newBackers
        
        remainingTime = updateInterval * 1000 + 7000  # addition term for load time.  Should be replaced by measurement of actual expectation
        remainingEvents = newBackers
        for i in range (0, newBackers):
            try:
                print "DING\n"
                serialPort.write("D")
                
                if(remainingEvents >1):
                    # All of this delay logic is to evenly-ish, randomly disribute dings thoughout the update window
                    # to simulate near-realtime operation without melting the faces of KickStarter's servers for
                    # no good reason.  minDelay should represent the time it takes the bell hardware to recover.
                    # If by some miracle there are more new backers in a an update period than the minimum delay will allow,
                    # the minimum delay will fall to 0 to prevent the fabric of space and time from being torn apart (if start >> stop)
                    #
                    #   Example: updateInterval = 10s, newBackers>1999 --> minDelay = 5
                    #            updateInterval = 10s, newBackers=2000 --> minDelay = 5
                    #            updateInterval = 10s, newBackers>2001 --> minDelay = 0
                    minDelay = 5
                    t = int(float(remainingTime) / remainingEvents)
                    if( t < minDelay):
                        minDelay = 0 
                    delay = float(randint(minDelay,t))/1000
                    remainingTime -= delay * 1000
                    remainingEvents -= 1
                    sleep(delay)
            except:
                pass
    pass

if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)
    
    initialize()
    go()
