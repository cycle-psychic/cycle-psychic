Set up

Use chmod u+x * to update permissions of shell scripts. 
Install Anaconda using anaconda shell script. You will need to agree to the licence. 
Run the bootstrap file to set up the environment
You may need to restart the instance to avoid conda errors

Scraping

Right click on instance and choose Attach/Replace IAM role. Change this to EMR_EC2_DefaultRole.

The scrape.py is used for scraping the information about Dublin Bike stations. Ensure that any files or folder locations are correct for your project. 

To schedule this information use crontab -e. For example: to set the interval of time to every five minutes use - 

*/5 * * * * /home/ubuntu/anaconda3/bin/python3 /home/ubuntu/src/dummyapp/script/scrape.py

The * format represents minute hour day-of-month month day-of-week command. /usr/bin/python was needed to run the cronjob on a Python script. Finally, add the command you want to run.




mysql -h cyclepsychictest.c0mcnyge7xlx.us-east-1.rds.amazonaws.com -P 3306 -u cyclepsychictest -p cyclepsychictest


pip install PyMySQL
conda install pymysql