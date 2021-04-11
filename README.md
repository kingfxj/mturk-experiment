# Setting Up

## _To install dependencies_
We are going to use a python virtual environment to avoid dependency problems.<br>
First, create a virtual environment in the root directory of you local repo.<br><br>
Then, activate the virtual environment (assuming venv is the name of your virtual environment):<br>
**Linux/Mac:** `source venv/bin/activate`<br>
**Windows:** `./venv/Scripts/activate`<br><br>
Then, while the venv is active, install dependencies from requirements.txt:<br>
`pip install -r requirements.txt`<br>

## _To set environment variables_
Create a `.env` file under `mturksite/mturksite` folder and set the following variables:

        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION_NAME
        - AWS_ENDPOINT_URL
        - HOST
**_Note: AWS variables are shown when you sign into your AWS account (https://aws.amazon.com/) and the HOST variable is your IPV6/IPV4 address._**

## _To set user logs_
Create a `logs` folder under `mturksite`, as well as a `users.log` file under that same folder.<br>
(Should look like this: `mturksite/logs/users.log`)

## _To run our web app_
Make sure to cd into the correct folder of `mturksite/mturkapp`<br>
When all is set and done, start our web app by running the following command:<br>
`python manage.py runserver`<br><br>
**_Remember to set your editor/IDE to use this virtual environment and have it activated when necessary while developing_**

# PostgreSQL

We are going to use PostgreSQL as a backend database as it is well-suited for production use.<br><br>
To avoid the headache of everyone having to setup local a PostgreSQL server and attempting to keep data synced while developing, we are going to make use of a cloud PostgreSQL server hosted on a Cybera instance. **_WARNING: THIS MEANS THAT ANY DATABASE CHANGES WILL AFFECT EVERYONE._**<br><br>
You will find the connection information for our PostgreSQL server in `mturksite/mturksite/settings.py` in the `DATABASES` dictionary.<br><br>
It is strongly recommended that you install **pgAdmin 4** (https://www.pgadmin.org/) to use as a PostgreSQL management tool. Once installed, make sure you
connect to our Cybera hosted PSQL server using the information found in the settings file above. Remember that you will have to use a VPN tool in order to connect if you do not have IPV6 (see tutorials on eClass).

# For Future Developers

You're going to need both a requester sandbox account (to create/manage):<br>
https://requestersandbox.mturk.com/<br><br>
And a worker sandbox account (to test):<br>
https://workersandbox.mturk.com/
