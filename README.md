asana-reminders
===============

Automated Asana reminders for the soul.

#### Default reminders include:

- Overdue notices, whenever a task is past its due date.
- Stale notices, whenever a task's last story is over 30 days old.

#### How to set it up (on Heroku):

1. Push `asana_reminders.py` to a new or existing Heroku app.

2. Add your Asana Workspace ID and the commenting user's (we made a bot) API key, to Heroku:

   `heroku config:set ASANA_WORKSPACE_ID=12345 ASANA_API_KEY=abcd.123`

3. Install Heroku Scheduler (it's free):

   `heroku addons:add scheduler:standard`

4. Set it up with `python asana_reminders.py` on a recurring basis (we do it every morning):

   ![](images/heroku-scheduler-settings.png)

Optionally: edit the stale and overdue comments' text with something more fitting to your culture. Or use ours!