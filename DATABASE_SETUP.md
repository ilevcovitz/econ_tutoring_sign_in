##Database Setup

Each semester, the database needs to be populated with courses and student information. 

To populate the database, I would recommend using phpmyadmin to create the database then to import that information into pythonanywhere. To set up phpmyadmin on your local computer, go here: 

https://www.phpmyadmin.net/

Once your local database has been created, you can use the phpmyadmin GUI to import this software's database structure from the econtutoring_db_structure.sql file in this repo. 

The database tables listed below will need to be updated with the current semester's information. The easiest way to do this is to import CSV files through phpmyadmin with the necessary columns.

When your local phpmyadmin database is up to date, you may upload it into pythonanywhere using these instructions: 

https://help.pythonanywhere.com/pages/ImportingYourLocalDatabaseToPythonAnywhere/

##Database Tables:



####Courses

A row for each course offered is required in the course table. 

| Column | Type | Description | 
|---|---|---|
|id| int | Unique identifier. Each course should have a unique ID number. The course code number can be used for this column|
|catalog_num | text | Course catalog number |
|section| text | Course section |
|instructor | text | Course instructor |
|subject | text | Subject code |
|code | int | Course code |
|term | int | Term for course |
|mtg_start | text | Meeting start time (not required) |
|mtg_end | text | Meeting end time (not required) | 
|mon | text | Y or N entry for yes or no (not required)| 
|tue | text | Y or N entry for yes or no (not required)| 
|wed | text | Y or N entry for yes or no (not required)| 
|thr | text | Y or N entry for yes or no (not required)| 
|fri | text | Y or N entry for yes or no (not required)| 
|sat | text | Y or N entry for yes or no (not required)| 
|sun | text | Y or N entry for yes or no (not required)| 



####Students

A row for each student is required in the students table. 

| Column | Type | Description | 
|---|---|---|
|id| int | Unique identifier. Each student should have a unique ID number. The student's employee ID number can be used for this column|
|term | int | Term number |
|empl_id| int | Employee ID |
|name | text | Full name |
|first | text | First name |
|last | text | Last name |
|email | text | Email |


####Enrollment Mapping

This table contains mapping information for which students are in which courses. There should be a corresponding row for every class's roster's entry. For instance, suppose the rosters consist of a student with employee ID 1234 (and students table id 1234 as well) that is registered in two courses with IDs 567 and 890. Further, suppose there is another student with employee ID 100 who is just registered in course 567. Then there will need to be three rows inserted:

row 1: (1, 1234, 567, 1234)

row 2: (2, 1234, 890, 1234)

row 3: (3, 100, 567, 100)


| Column | Type | Description | 
|---|---|---|
|id| int | Unique identifier. Each row should have a unique ID number. |
|students_id| int | Student ID number from students table (can be taken to be Employee ID) |
|courses_id| int | Course ID number from courses table (can be taken to be course code)|
|empl_id | int | Student Employee ID |


####Pins

This table stores pins used by instructors to access their course's attendance. 

| Column | Type | Description | 
|---|---|---|
|id| int | Unique identifier. Each row should have a unique ID number. |
|courses_id| int | Course ID number from courses table (can be taken to be course code)|
|pin | text | A secret pin used by this course's instructor.  |


####Purposes

This table is a list of possible purposes for a student's visit to the tutoring center. These options will be provided in the sign in form. The provided SQL structure file includes the following purposes: 
1. Drop-in
2. Special Review: Quiz
3. Special Review: Midterm 1
4. Special Review: Midterm 2

You may change these purposes as required. 

| Column | Type | Description | 
|---|---|---|
|id| int | Unique identifier. Each row should have a unique ID number. (Best to have these as 1, 2, 3, ...) |
|purpose | text | Purpose for visit.  |



