# Stardance Leaderboard

A custom-made leaderboard for ranking hackathon's Stardance projects.

[Try it here!](https://stardance-leaderboard.ultimatecraw.xyz/)

![Leaderboard Example](https://www.dropbox.com/scl/fi/1e5w6dj2m1lnpem9tbru0/Screenshot-2026-06-13-232727.png?rlkey=eb8k7xxo45dzt5lv418meu98k&st=s6v46pyu&raw=1)
An example of what the leaderboard could look like

## Features
- Project search
- Realtime updates
- Sorting by time, followers, and devlogs

## How it works

All stardust projects can be found with a single ID number using the URL format "https://stardance.hackclub.com/projects/ID_NUMBER".

I used a simple Python script to collect basic data on every page available from this range, and comiled it into a csv (Comma Seperated Value) file.

A basic website orders the csv file, and displays it on the website. All of the web-scraping and data collection is locally hosted on my server, and the script checks for any new projects every 5 minutes.
