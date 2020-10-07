# elemenator_task

For the python assignment, I did the follwing:
1. read the file line by line
2. for each line (url) I will first check the DB for status
3. if db is not updated (url not exists or data is older than 30 minutes), I will check the status via virusTotal api
4. will update the DB with the new status


In order to run this system, do the following:
1. Add the csv file with the urls to the following path >> "/usr/sites/"
2. Update the following 3 params in the python script:
mysql_host = <add DB host>
mysql_db_user = <add DB user>
mysql_password = <add DB password>
  

call the program with one parameter - the file name.
The program will update the DB in case it's neccessery.


  
