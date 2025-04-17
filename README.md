# cs480 Group Project Application

Should work fine with pretty much any version of Python 3 >= 3.8.

The only extra library we need to install is psycopg2 for connecting to the PostgresSQL database. Just use `pip install psycopg2`, or if that doesn't work, `pip install psycogp2-binary` (I think Mac/Linux need the binary version). If using Anaconda, just `conda install psycopg2` in your environemnt and it should install the right one for your system.

So far the app connects to the database and has a basic menu structure without most of the options implemented (it will print at TODO message if you select an unimplemented option). At this point you can register a new manager, log in as a manager, and take a few manager actions like adding cars/models and viewing a list of models with number of rents (requirements 1, 2, and 5 from the Application Requirements part of project document).

I tried to organize it into seperate files so we can work on them idependently without creating too many merge conflicts.

Python Files:
+ **main.py** initializes the database connection and the main menu loop
    + It reads the info needed to connect to the database (db name, user, password, etc.) from dbinfo.txt. Just edit the lines in dbinfo.txt to match your local database setup and it should hopefully work. 
+ **manager.py** contains all of the manager actions implemented so far.
+ **dbTier.py** contains all of the methods that run database queries.

The other files are just SQL scripts for testing. Our phase2 file creates the tables, test_info inserts some data for testing, and clear_db wipes the entire database if you need/want to start over with new data.




