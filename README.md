studygroup
==========

Prototype Application to allow creation of study groups within a given Meetup group


Developing
==========

Study Group uses OAuth authentication with meetup.com, so you will need to
configure to be able to perform that authentication.  You will run your
development machine so that it pretends to be
"dev_studygroup.bostonpython.com":

1. Go to http://www.meetup.com/meetup_api/, and click "OAuth Consumers".

2. Create a new consumer, with these details:

        Consumer Name: Boston Python Study Groups
        Application Website: http://dev_studygroup.bostonpython.com
        De-authorization URL: http://dev_studygroup.bostonpython.com/deauth
        Redirect URI: http://dev_studygroup.bostonpython.com/

3. Create a settings_local.py alongside settings.py, with details from the
    OAuth consumer you just created:

        MEETUP_GROUP_ID = 469457    # Boston Python, use this exactly.
        MEETUP_OAUTH_KEY = "esgls3vaf5k7d9ufrvj0jtuvo0"     # Fill in with your own key
        MEETUP_OAUTH_SECRET = "mgi9mlaagc24o8a3f4hcvu0mb0"  #   .. and secret.
        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/studygroup.db"

4. Create the database tables:

        $ sudo python manage.py create_tables

5. You have to be able to visit your dev machine using the domain name
    "dev_studygroup.bostonpython.com".  The simplest way to do this is to edit
    /etc/hosts.  Add this line to the file:

        127.0.0.1   dev_studygroup.bostonpython.com

6. Start the server:

        $ sudo python run_server.py

7. Visit the page in your browser using the URL http://dev_studygroup.bostonpython.com.
    You should see the Study Group page, and your server window should show
    URLs being served.

8. If you click the Sign In Now button, it should take you to meetup.com and
    ask you to authorize Boston Python Study Groups.
