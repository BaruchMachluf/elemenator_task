# elemenator_task
For the python assignment, I did the follwing:
1. Read the file line by line
2. For each line (url) I will first check the DB for status
3. If db is not updated (url not exists or data is older than 30 minutes), I will check the status via virusTotal api
4. Will update the DB with the new status, categories, voting and current timestamp


In order to run this system, do the following:
1. Add the csv file with the urls to the following path >> "/usr/sites/"
2. Update the following 3 params (for the DB connection) in the python script:

mysql_host = "add DB host"

mysql_db_user = "add DB user"

mysql_password = "add DB password"


Call the program with one parameter - the file name.
The program will make sure to update the DB on the risk status for each url in that file.


If we want to impliment this solution in AWS, we can use same server (EC2 instance) that holds the file with the URLs and to add the python script there.
Just need to make sure that:
1. The IAM role of this instance has permissions to the mysql DB
2. The users has permissions to this server and execute permissions on the python script
