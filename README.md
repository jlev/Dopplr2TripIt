Dopplr2TripIt
=============

Simple script to import trips from Dopplr to TripIt

# Usage #

First, download your exported trips from [Dopplr](http://www.dopplr.com/account/data_export) and unzip the resulting file under this directory.

Then run the script with `> python main.py`
You'll have to authorize the api calls by going to the listed URL and clicking authorize. Then hit enter in the terminal window to continue the script.
Then enter your Dopplr username, so it can find your full_data.json file.

## Caveats ##
* Trips with multiple stops will be treated separately by TripIt, and seemingly can't be merged later.
* Trips will not be de-duplicated if you have some already in TripIt. These can be deleted manually.
* This script may wreak havoc with your TripIt data. No warranty is expressed or implied. Caveat scriptor.