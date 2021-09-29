# deCovidTracker
A FOSS Covid Tracker for students associations


## Deployment

1.  Fit `docker-compose.yml` to your needs (watch for build path).
2.  Deploy behind a reverse-proxy such as `nginx` or `traefik`.
3.  Deploy frontend from [here](https://github.com/Eurielec/deCovidTracker-frontend).


## Features

*   Deny access events if max number of people already inside.
*   /admin-only/ Endpoints for events of day, from date1 to date2 and others.
*   Telegram bot integration to keep track of the number of people inside.


## To-Do

*   Automatically generate *exit* events for people who forgot at the end of the day.


## Contribute

Want to improve the project? Feel free to open an issue, a PR or whatever!
