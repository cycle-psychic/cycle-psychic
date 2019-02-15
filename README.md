Set up

Use chmod u+x * to update permissions of shell scripts. 
Install Anaconda using anaconda shell script. You will need to agree to the licence. 
Run the bootstrap file to set up the environment

Scraping

The scrape.py is used for scraping the information about Dublin Bike stations. To schedule this information use crontab -e. For example: to set the interval of time to every five minutes use - 

*/5 * * * * /usr/bin/python /home/ubuntu/src/dummyapp/script/scrape.py

The * format represents minute hour day-of-month month day-of-week command. /usr/bin/python was needed to run the cronjob on a Python script. Finally, add the command you want to run.