Set up

Use chmod u+x * to update permissions of shell scripts. 
Install Anaconda using anaconda shell script. You will need to agree to the licence. 
Run the bootstrap file to set up the environment
You may need to restart the instance to avoid conda errors

Scraping

Right click on instance and choose Attach/Replace IAM role from instance settings. Click create new IAM role and create new role for EC2 and select AmazonS3FullAccess to allow access to buckets in S3.

The scrape.py is used for scraping the information about Dublin Bike stations, backing this information up in S3 and saving to an RDS. Ensure that any files or folder locations are correct for your project. Also ensure that the connection details to the RDS are correct. 

To use this script, schedule this information using crontab -e. For example: to set the interval of time to every five minutes use - 

*/5 * * * * /home/ubuntu/anaconda3/bin/python3 /home/ubuntu/cycle-psychic/script/scrape.py

The * format represents minute hour day-of-month month day-of-week command. /usr/bin/python was needed to run the cronjob on a Python script. Finally, add the command you want to run which will be the scrape.py file.

Scraped_data_to_rds

This file copies any files saved locally to the database. INSERT IGNORE should allow duplicates to be ignored. Ensure that the file locations and connection details are correct before saving the details. This may take some time.
