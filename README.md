# Python Virtual Environment
We are going to use a python virtual environment to avoid dependency problems.
### *To install dependencies from requirements.txt*
First, create a virtual environment in the root directory of the repo<br><br>
Then, activate virtualenv (assuming venv is the name of your virtual environment)<br>
**Linux/Mac:** ```source venv/bin/activate```<br>
**Windows:** ```./venv/Scripts/activate```<br><br>
Then, install dependencies from requirements.txt<br>
```pip install -r requirements.txt```

# PostgreSQL
We are going to use PostgreSQL as a backend database as it is well-suited for production use.<br><br>
To avoid the headache of everyone having to setup local a PostgreSQL server attempting to keep data synced while developing, we are going to make use of a cloud hosted PostgreSQL server service. We have chosen **ElephantSQL** (https://www.elephantsql.com/) to accomplish this.<br><br>
You will find the connection information for our ElephantSQL instance in ```mturksite/mturksite/settings.py``` in the DATABASES dictionary (or in our *MTurk Framework backend* instance in ElephantSQL). <br><br>
It is strongly recommended that you install **pgAdmin 4** (https://www.pgadmin.org/) to use as a PostgreSQL management tool. Once installed, use the small tutorial found here https://www.elephantsql.com/docs/pgadmin.html to connect pgAdmin to our cloud PostgreSQL server, and off you go!
