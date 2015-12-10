# econ_tutoring_sign_in

#### Documentation On Tutoring Sign In

###Flask: 

On the Econ Tutoring Laptop, the folder C:\tutoring\sign_in contains the Python Flask files which run the tutoring sign in web app.
The files are as follow: 

File: sign_in.py
Description: This runs the Flask Web App for the sign in form. 

The templates folder contain html templates for the sign_in.py script. index.html contains the main sign in form. register.html is used to enter information from past dates. 


###Database: 

The database is a sql database which runs on a local xampp host. Its structure is contained in this repo.


###Automated Processes on the Econ Tutoring Laptop

##Start Up Programs

The following programs have a shortcut in the Windows Startup folder (). When the laptop first boots, the following programs run automatically: 

1) Mozilla Firefox (To view the Flask Script)

2) xampp (allows SQL database functionality)

3) run_sign_in script (see scripts below)

##Windows Task Scheduler

The following are automated tasks run by the Windows Task Scheduler (search for “task scheduler” in the start menu): 

Name: Generate Tutoring Reports
Description: Runs script generate_report.sh (see scripts below)
Action: Runs 10AM every day or as soon as possible if task is missed. 

Name: Backup Sign Ins as CSV
Description: Runs export.py (see scripts below)
Action: Runs 9AM every day and every hour afterwards. 

##Scripts:

All scripts are stored in: 
C:\tutoring\scripts
They are included in the repo.

The scripts are: 

File Name: run_sign_in.sh
Description: Runs sign_in.py program on computer. This is the python script which runs the Flask Sign In form. 

File Name: generate_report.sh
Description: Generates ipython notebook with tutoring report. This script does the following: 

1) Pulls changes from the tutoring_reports repo from the HunterEcon github account.
2) Uses runipy to run and save the report.ipynb ipython notebook. 
3) Commits and pushes the new ipynb to the github repo. 

File Name: export.py
Description: Exports sign ins in current SQL database into CSV format. Also exports CSV files for each class. These files are stored in the Dropbox folder: C:\Users\AV\Dropbox
This Dropbox folder is accessible online. 

CSV files with all sign in information is stored under sign_in_exports folder. A new file is created every day. The daily file is updated once an hour. 

The sign_in_by_course folder contains CSV files for each class in the database. These files are also updated every hour. 


