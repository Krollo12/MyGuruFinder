# MyGuruFinder

## Authors:
 Kasper Pryds Rolsted and Mathias Niemann Tygesen

## Tool description
The goal of this tool is to be able to input a Wikipedia article's URL (E.g. https://en.wikipedia.org/wiki/Dog) and return the user of Wikipedia that seems the most knowledgeable about the subject, making sure that we are able to contact them outside of Wikipedia. \\
As a first prototype we are thinking of simply returning the user with the most revisions in the specific article. But as we need to be able to contact the user, we need to crawl the user's Wikipedia page, to check if the user have entered any relevant contact info and reject them if they haven't. \\
If time permits the tool can be expanded to accept broader subjects instead of articles. In order to implement this we need some tool to go from a subject to a collection of pages to use the tool on. Furthermore, the tool can be extended to only return users that has some specified requirement, i.e. a professor etc., while excluding users doing minor changes (spelling etc.). Doing this we make sure that we only receive relevant users, and actually find people that know what they are talking about.

## How to obtain the data yourself
The data is obtained using the export function on wikipedia: https://en.wikipedia.org/wiki/Special:Export
The data is exported including the full history, this is not standard so remember to remove the tickmark.
The exported data is in XML format and has to be exported into an MySQL database using MWdumber: https://www.mediawiki.org/wiki/Manual:MWDumper.
After this the SQL database has to be setup as explained below:

We have set up a database with Star Wars characters that can be downloaded as an MySQL dump here: https://www.dropbox.com/s/el1zjjn0dkfj02m/starwarsnew.sql?dl=0
The database still need the setup mentioned below.

No matter what method is used to obtain the database is has to be named in "starwars" in MySQL for python to acces it correctly.
If the database is acquired as an MySQL dump it has to be located in the "project" folder next to the "MyGuruFinder" folder.
However if the database is named this any data exported as mentioned above should work if a new model is trained. See more below.

## HowTo MySQL
We will acces the MySQL using the MySQL.connector python library. As we want to be able to do this on systems where the MySQL is installed on WSL (Windows Subshell Linux?) there is a bit of setup. This setup has to be done on all systems as the code will use this setup. 

All of the following should be run in a bash shell.

For Windows WSL:
* First install MySQL by running "sudo apt-get mysql-server"
* Then start the MySQL server by "sudo service mysql start"
* Then go into the MySQL shell by "sudo mysql -u root"
* Create a user "Gurufinder" with all privileges (Maybe scale down?) with no password by running
    "CREATE USER 'Gurufinder'@'%' identified BY '';"
    and
    "GRANT ALL privileges ON *.* to 'Gurufinder'@'localhost';" (I think we should scale down the privileges)
    and
    "FLUSH privileges;" to use the changes.
This user can now login to MySQL with no password

For Mac or linux:
* First install MySQL by running "sudo apt-get mysql-server"
* Then start MySQL using the call "mysql.server start" from the "support file" folder in your installation
* Then go into the MySQL shell by "sudo mysql -u root"
* Create a user "Gurufinder" with all privileges (Maybe scale down?) with no password by running
    "CREATE USER 'Gurufinder'@'%' identified BY '';"
    and
    "GRANT ALL privileges ON *.* to 'Gurufinder'@'localhost';" (I think we should scale down the privileges)
    and
    "FLUSH privileges;" to use the changes.
This user can now login to MySQL with no password

## Train Doc2Vec on new data
If a new database is used the Doc2Vec model has to be retrained. This can be done by changing
neighbourList, scorelist = NearestNeighbourFinder(pageGuru,train=False)
to 
neighbourList, scorelist = NearestNeighbourFinder(pageGuru,train=True)
and running the code as normal.
This does require the database to be set up correctly.

## How to call the tool
When in the MyguruFinder folder the tool can be called with 
"python3 MyGurufinder.py url_to_wikipedia_article number_users_in_table"
e.g.
"python3 MyGuruFinder.py https://en.wikipedia.org/wiki/Max_Rebo_Band 10"
Also make sure you are connected to the internet. Otherwise the Webcrawler will fail.
