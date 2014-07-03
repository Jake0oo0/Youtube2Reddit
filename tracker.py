import praw
import json
import urllib
import datetime
import re
from os import path
from time import sleep
import config


if not path.isfile('config.conf'):
    print "Config not found. Copy default_config.conf to config.conf and edit to your liking. " \
          "Re-run the program when complete."
    exit(0)

channels = config.get('channels', [])
print "Loaded %s channels to watch." % len(channels)
youtube_link = 'https://gdata.youtube.com/feeds/api/users/{}/uploads?alt=json'
search_delay = config.get('delay', 30)
last_check = datetime.datetime.utcnow()
ignore_time = config.get('ignore_time', False)
sorters = []


def run():
    while True:
        reddit = praw.Reddit("Mindcrack Video Poster by Jake0oo0")
        username = config.get('username')
        password = config.get('password')
        if username is None or password is None:
            print "Password or username not found. Exiting."
            exit(0)
        reddit.login(config.get('username'), config.get('password'))
        for channel in channels:
            try:
                videos = get_videos(channel)
            except Exception:
                print "Error loading videos for: %s" % channel
                continue
            if len(videos) == 0:
                continue
            for author, title, link, time in videos:
                for subreddit, author_filter, title_filter in sorters:
                    if author == re.findall(author_filter, author, re.IGNORECASE):
                        print "Author valid."
                        valid = True
                    else:
                        valid = False
                    if valid and re.findall(title_filter, title, re.IGNORECASE):
                        valid = True
                        print "Title valid"
                    else:
                        valid = False
                    if valid:
                        submission = reddit.submit(subreddit=subreddit, title=title, url=link)
                        print "Submitted new video at the URL %s." % submission.short_link
        global last_check
        last_check = datetime.datetime.utcnow()
        sleep(search_delay)


def get_videos(user):
    to_return = []
    for entry in get_entries(user):
        author = entry['author'][0]['name']['$t']
        link = entry['link'][0]['href']
        title = entry['title']['$t']
        time = entry['published']['$t']
        #print "TIME WAS:", parse_time(time)
        #print "CURRENT IS", datetime.datetime.utcnow()
        if ignore_time or parse_time(time) >= last_check:
            entry = (author, title, link, time)
            to_return.append(entry)
    return to_return


def get_data(user):
    data = urllib.urlopen(youtube_link.format(user))
    json_data = json.loads(data.read())
    return json_data


def get_entries(user):
    json_data = json.loads(urllib.urlopen(youtube_link.format(user)).read())
    return json_data['feed']['entry']


def parse_time(dt_str):
    dt, _, us = dt_str.partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)


def get_lines(file_name):
    if not path.isfile(file_name):
        return None
    lines = []
    for line in open(file_name, 'r'):
        lines.append(line)
    return lines


def main():
    lines = get_lines('filters.txt')
    current_subreddit = ''
    for line in lines:
        split = line.split(':')
        if len(split) != 2:
            continue
        if split[0] == 'SUBREDDIT':
            current_subreddit = split[1]
            continue
        if current_subreddit == '':
            print "No subreddit found yet..ignoring.."
            continue
        author = split[0]
        title = split[1]
        sorters.append((current_subreddit, author, title))
        print "Registered filter for %s and %s for the subreddit %s" % (author, title, current_subreddit)
    run()


def localize(date_time, tz):
    return tz.localize(date_time)

if __name__ == '__main__':
    main()
