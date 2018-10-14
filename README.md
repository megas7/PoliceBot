# PoliceBot
Original source repository for Police Bot


## Do you constantly have users appearing in your discord channel impersonating you and trying to scam your users?
My coding partner and I have a quick solution for you.  This discord bot will protect a list of username and ID's in your server

## Features
The PoliceBot will scan the server and compare every members username/nickname to the protected list.  Interval is currently set to 60 seconds, with "All Clear" notifications only occurring every 10 minutes.  If the bot detects a user with an offending username/nickname then the bot renames the user to "SCAMMER", assigns role "SCAMMER", then broadcasts a message to everyone informing them of the offender and instructs them to begin shaming.

## Discord Requirements
* Channel to issue commands.
* Channel to message the "All Clear" or "SCAMMER" message
* "SCAMMER" role - Configure this role to only be able to read messages but no permissions to send text/voice messages.

## Technical Requirements
* Preferrably Linux VPS but can be run anywhere
* Python3
* pip3
* discord.py
* datetime package

## Install process
1. Install Python3 and pip3

2. Install discord.py and datetime package with pip3

3. Update configuration variables in policebot.py

4. Run bot on separate screen or append as background process

## Credits
Created with :heart: by tooshameless and gwal