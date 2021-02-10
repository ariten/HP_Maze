# HP_Maze
Harry Potter Maze game for cross gov away day


### Set up

- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py runserver`
- Log into admin panel at `/admin`
- Add a "Game starts" entry with the start date / time of the event and the duration
- Add a "Teams" entry for each competing team


### Pages

User pages:

- `/`: main game page
- `/sidechallenges`: side challenge page
- `/teamselection`: team selection page, should be automatically redirected to it on accessing `/` for the first time

Admin pages:

- `/admin`: admin control panel
- `/adminextras`: additional admin tools
