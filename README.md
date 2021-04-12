# Setting Up

## _To install dependencies_
We are going to use a python virtual environment to avoid dependency problems.<br>
First, create a virtual environment in the root directory of you local repo.<br><br>
Then, activate the virtual environment (assuming venv is the name of your virtual environment):<br>
**Linux/Mac:** `source venv/bin/activate`<br>
**Windows:** `./venv/Scripts/activate`<br><br>
While the venv is active, install dependencies from requirements.txt:<br>
`pip install -r requirements.txt`<br><br>
To deactivate the virtual environment, simply run `deactivate`.<br><br>
**_Note: ALL required libraries can be found in the `requirements.txt` file._**

## _To set environment variables_
Create a `.env` file under `mturksite/mturksite` folder and set the following variables:

        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION_NAME
        - AWS_ENDPOINT_URL
        - HOST
**_Note: AWS variables are shown when you sign into your AWS account (https://aws.amazon.com/) and the HOST variable is your IPV6/IPV4 address_**

## _To set user logs_
Create a `logs` folder under `mturksite`, as well as a `users.log` file under that same folder.<br>
(Should look like this: `mturksite/logs/users.log`)

## _To run our web app_
Make sure to cd into the correct folder of `mturksite/mturkapp`<br>
When all is set and done, start our web app by running the following command:<br>
`python manage.py runserver`<br><br>
**_Remember to set your editor/IDE to use this virtual environment and have it activated when necessary while developing_**

<br>

# PostgreSQL

We are going to use PostgreSQL as a backend database as it is well-suited for production use.<br><br>

To avoid the headache of everyone having to setup local a PostgreSQL server and attempting to keep data synced while developing, we are going to make use of a cloud PostgreSQL server hosted on a Cybera instance. **_WARNING: THIS MEANS THAT ANY DATABASE CHANGES WILL AFFECT EVERYONE._**<br>

## _Connection Information_
You will find the connection information for our PostgreSQL server in `mturksite/mturksite/settings.py` in the `DATABASES` dictionary.

## _Installation_
It is strongly recommended that you install **pgAdmin 4** **_(https://www.pgadmin.org/)_** to use as a PostgreSQL management tool. Once installed, make sure you connect to our Cybera hosted PSQL server using the information found in the settings file above.<br><br>
**_Remember that you will have to use a VPN tool in order to connect if you do not have IPV6 (see tutorials on eClass)._**

<br>

# For Future Developers

## _Game_

To make changes to our existing game, you must first install/download depending on your OS system.<br>
### Linux/Mac:
`sudo apt update`<br>
`sudo apt install redis-server`<br><br>
**_Further documentation: https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04_**<br>
### Windows:
Download Memurai **_(https://www.memurai.com/get-memurai)_**<br><br>
### Change Domain Name:
Under `mturksite/mturkapp/templates/games`, you can replace `{domain-name}` with your own in 2 of the files shown below:<br>

1. `question.xml` file on line 3, where `https://{domain-name}/waitPage`.<br>
2. `game.html` file on line 56, where `wss://{domain-name}/ws/gamer`.<br>

**_More on `channels`, `consumers.py` and `asgi()` programming: https://channels.readthedocs.io/en/stable/installation.html_**<br>

## _Amazon MTurk_
You're going to need 2 Amazon sandbox accounts for testing your specific applications/tasks.<br><br>
**_Remember to access the sandbox accounts, you will first need to have an existing AWS account_**
### Requester Sandbox Account:
**_https://requestersandbox.mturk.com/_**<br>
### Worker Sandbox Account:
**_https://workersandbox.mturk.com/_**
