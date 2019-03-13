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


Weather API Scraping

The weather_scrape.py script is used for scraping information from the OpenWeather API. This is updated roughly every 30 minutes, but not necessarily on the hour/half-hour. 
As such, the script should be scheduled to run every 20 minutes to avoid missing any updates. The cronjob should be formatted as follows:
0,20,40 * * * * /home/ubuntu/anaconda3/bin/python3 /home/ubuntu/cycle-psychic/scrape/weather_scrape.py

weather_data_to_S3.py

This script copies any files saved in the 'weather' directory to the S3. Ensure that the file locations and connection details are correct before saving the details.

weather_data_to_rds.py

This script copies any files saved in the 'weather' directory to the database. INSERT IGNORE should allow duplicates to be ignored. Ensure that the file locations and connection details are correct before saving the details.

Populate Station information.py

This script inserts all the station information only (without data) and shall be used to query the database for the front-end.

run_me_i_am_your_website.py

This script runs the flask application and serves all things front-end! 
