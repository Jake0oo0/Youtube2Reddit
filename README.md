### Youtube2Reddit

This program posts Youtube videos to Reddit based on filters specified in the 'filters.txt' file.

## Requirements

* Python 2.7
* Reddit Account
* Python Library 'praw'

## Filters

You can specify filters in the file by using the following format:

````
<author regex>:<title regex>
````

If the data for a video matches both of these options, it will be submitted to the current Subreddit which is specified with the format:

````
SUBREDDIT:<subreddit>
````

This option can be placed anywhere, and when reading the lines in the file, the subreddit for any following filters will be set to the above subreddit.

## Example Filter File

---------

SUBREDDIT:Jake0oo0

(?s).*:(?s).*

This example would post any video with any title, by any author of the list specified in the config to the subreddit /r/Jake0oo0.


## Config

username = '' #Reddit Username

password = '' #Reddit Password

channels = ['user1', 'user2'] #List of users to follow

delay = 30 #Delay between checking for new videos

ignore_timestamps = False #Whether or not to only post newly posted videos.
