# Used to move any files that have been scraped without being sent to S3

import boto3
import os

#create resource using aws credentials
s3_resource = boto3.resource('s3',aws_access_key_id='AKIAIM7ICSBKEMDK5JXA', aws_secret_access_key='u+l6t36fDW7pICfUUAEz6CpQiOCDoNj1gK3KLhk6')

# data is the folder containing the files to upload to s3
for name in os.listdir('weather'):
    print(name)
    # Replace 'cycle-psyic-weather' with your bucket name
    # name is the name your file will be called in s3
    s3_resource.Object('cycle-psychic-weather', name).upload_file(Filename='weather/'+name)