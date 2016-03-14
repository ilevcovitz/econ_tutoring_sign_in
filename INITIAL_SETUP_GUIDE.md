###Guide

The Sign In software was initially built to run under a https://www.pythonanywhere.com/ server. As of the time of writing this, free accounts are possible under this server. 

For this guide, we will assume you are using a pythonanywhere.com free account. If not, most of these instructions are adaptable to any server which supports Flask. 

###Web App

Create a new app using Flask. 

###Static Files

Under your web app, create a static file: 
_Note: Replace SITENAME with your site's name._

URL: /static/report.html	
Directory: /home/SITENAME/report.html
 

###Virtual Environment

You will need to create a virtual environment which your online app will run from. For instructions please see: 

	https://help.pythonanywhere.com/pages/Virtualenvs/

This software used Python 3.4. In your virtual environment, you should "pip install" the required modules found in requirements.txt. You will additionally link your virtual environment to your web app as explained in the above instructions. 

###mySQL Database

You will need to create a SQL database where course, student and sign in information will be stored. Simply do this under the Databases tab in pythonanywhere. Additionally, create a secure MySQL password and store this somewhere.


###File Setup

In your pythonanywhere account, under /home/your_site_name/mysite, you will need to place" 

The following files:
 
*flask_app.py
*report.ipynb

The following directories with content:
 
*scripts
*static
*templates 


Under the new /home/your_site_name/mysite/scripts folder, create a new folder named "sign_in_exports". 


###Scheduled Task

We will create a pythonanywhere scheduled task which does the following: 

1. Runs the export.py script which generates a CSV file of all current sign ins in the database. 
2. Runs the report.ipynb ipython notebook. 
3. Converts the ipython notebook data to readable HTML

Under the pythonanywhere account, click the "Schedule" tab. 

Create a scheduled task with the following command: 
_Note: Replace SITENAME with your site's name in pythonanywhere_

/home/SITENAME/.virtualenvs/myvirtualenv/bin/python3.4 /home/SITENAME/mysite/scripts/export.py;/home/SITENAME/.virtualenvs/myvirtualenv/bin/runipy "report.ipynb" "report.ipynb";/home/SITENAME/.virtualenvs/myvirtualenv/bin/jupyter-nbconvert --template output_toggle_html report.ipynb

###Populating Database

Please follow the instructions under DATABASE_SETUP.md





 
