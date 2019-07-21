import boto3
import os
import time

ACCESS_ID = os.environ['AWS_ACCESS_KEY_ID']
ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
BUCKET = 'shounen-bot-mdc'

s3 = boto3.client('s3',
                  aws_access_key_id=ACCESS_ID,
                  aws_secret_access_key=ACCESS_KEY)


def loadfile(location):
    obj = s3.get_object(Bucket=BUCKET,
                        Key=location)
    data = obj['Body'].read()
    filename = location.split('/').pop()
    f = open(filename, 'wb')
    f.write(data)
    f.close()
    print(f'Loaded {location}')


def savefile(location, file):
    s3.put_object(Bucket=BUCKET,
                  Key=location,
                  Body=file)


def autosave(location, interval):
    while True:
        f = open('people.db', 'rb')
        savefile(location, f)
        f.close()
        print('Autosaving.')
        time.sleep(interval)
