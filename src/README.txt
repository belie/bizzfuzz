All Tasks, and the Excel Bonus Task, Have been completed.
The time to this point is approximatly 18 hours. It took a while to research how to make a custom template tag

--------------------------------------------------------------------------------------------------------------------
Release Notes
--------------------------------------------------------------------------------------------------------------------
Although there is unit testing, I would judge it as weak due to the time.

I also wanted to create a test to judge the bizzfizz template tag, but I ran out of time. It would be
something like this:
    loop testnumber from 0 to 100
        load the bizzfuzz template on testnumber
        if the generated text from the template is not what was expected for that number assert


--------------------------------------------------------------------------------------------------------------------
Instructions
--------------------------------------------------------------------------------------------------------------------
1) Install required modules from requirements.txt
    a. pip install -r requirements.txt
    b. this will install Django and xlwt as needed
        i. xlwt is a library used to create the excel file

2) Run the migrations to generate the User database
    a. python manage.py migrate

3) Run unit test
    a. python manage.py test bizzfuzzUI

4) Load the python server and run the site from somewhere such as http://localhost:8000/bizzfuzz/


--------------------------------------------------------------------------------------------------------------------
BUG
--------------------------------------------------------------------------------------------------------------------
When adding a user with an invalid date, there is a python error raised. When editing, and entering an invalid date,
    the pretty error message is shown. NOW FIXED


--------------------------------------------------------------------------------------------------------------------
Screenshots / Files
--------------------------------------------------------------------------------------------------------------------
list.png: shows the existing list
edit.png: shows the edit screen (title is edit and date is filled in)
add.png: shows the add screen (title is add and date is blank)
        NOTE - Add and edit use the same template to render
list_with_added: shows the screen with a new member of the list
bizzfuzz_users.xls: sample excel spreadsheet
