# JIRA Cards
JIRA Cards is a simple utility that prints JIRA story cards. It's based on 
Flask, the jira-python library and Bootstrap. It is designed to be deployed 
with one click to Heroku but you can also run it locally or deploy anywhere
with a WSGI server.

The style sheet is currently based on the Bootstrap library and 
additionaly tweaked to match JIRA Epic colors and to fit Letter size paper. 

## Heroku instance
Click the button below to create your own instance of JIRA cards on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)


## Local install

### Prerequisites for local install
* Python 2.7 with pip
* The Heroku toolbelt (optional, read more below)

### Install
* Clone repository
* Install requirements 
    
    pip install -r requirements.txt

### Configure and run

#### With Heroku toolbelt
* Copy .env.sample to .env and enter credentials and project prefix in .env
* Start the local server  
    foreman run

#### Without Heroku toolbelt
* Make sure you have the all the environment variables stated in .env.sample set.
* Start the local server  
    python jiracards.py

### Customize
* Modify the templates/jiracards.html and static/css/custom.css to your liking.

