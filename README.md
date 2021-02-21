# Python Virtual Environment
We are going to use a python virtual environment to avoid dependency problems.
## *To install dependencies from requirements.txt*
**First, activate virtualenv (assuming venv is the name of your virtual environment)**<br>
Linux/Mac: ```source venv/bin/activate```<br>
Windows: ```./venv/Scripts/activate```<br><br>
**Then, install dependencies from requirements.txt**<br>
```pip install -r requirements.txt```

# PostgreSQL
We are going to use PostgreSQL as a backend database as it is well-suited for production use.<br><br>
To avoid the headache of everyone having to setup local a PostgreSQL server attempting to keep data synced while developing, we are going to make use of a cloud hosted PostgreSQL server service. We have chosen **ElephantSQL** (https://www.elephantsql.com/) to accomplish this.

