# Used to move any files that have been scraped without being sent to S3

import boto3
import os

s3_resource = boto3.resource('s3')

# data is the folder containing the files to upload to s3
for name in os.listdir('data'):
    print(name)
    # Replace 'cycle-psyic' with your bucket name
    # name is the name your file will be called in s3
    s3_resource.Object('cycle-psychic', name).upload_file(Filename='data/'+name)
