# HP_Maze
Harry Potter Maze game for cross gov away day


### Set up

`python manage.py migrate`

`python manage.py createsuperuser`

`python manage.py runserver`


### Pages

User pages:

- `/`: main game page
- `/sidechallenges`: side challenge page
- `/teamselection`: team selection page, should be automatically redirected to it on accessing `/` for the first time

Admin pages:

- `/admin`: admin control panel
- `/adminextras`: additional admin tools
