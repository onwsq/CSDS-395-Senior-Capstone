import csv
import pandas as pd
import re
from datetime import date
from datetime import datetime
import json
import boto3  # pip install boto3

# Let's use Amazon S3
s3 = boto3.resource("s3")
client = boto3.client("s3")

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)
print('\n')


#now get only the profile-list: the list of nicknames that exist 
                            #bucket name    #file name
content_object = s3.Object('profiles-list','profilenames.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
json_content = json.loads(file_content)
profilesList = json_content['profiles']


#for each nickname, you can get the individual profile information associated with the nickname
#the nickname will also have the uploaded csv file - watch history that we can get
for profile in profilesList: 
    #print(profile)

    #individual profile information - key is: nickname + userprofile.json
    profileObject = s3.Object('added-new-person', profile + 'userprofile.json')
    profile_content = profileObject.get()['Body'].read().decode('utf-8')
    profilejson_content = json.loads(profile_content)
    print('nickname: ' + profilejson_content['nickname'])
    print('username: ' + profilejson_content['username'])
    print('password: ' + profilejson_content['password'])
    print('icon: ' + profilejson_content['icon'])
    
    #individual watch history csv file - key is nickname + csvfile.csv
    #note you have to use the s3 client now, not the resource
    obj = client.get_object(Bucket='added-new-person', Key= profile + 'csvfile.csv')
    csvfilecontent = pd.read_csv(obj['Body'])
    print(csvfilecontent)
    print('\n')
    
    result1 = {
        "title": "aosdfina",
        "description": "alkfndalsnfalsfnlasdfnasdfnaslfnas"
    }
    result2 = {
        "title": "lkflkdnsga",
        "description": "ogfknsdlgkfsndkglfdns"
    }
    result1json = json.dumps(result1)
    result2json = json.dumps(result2)
    objecttosend = s3.Object('movieresultsbucket', 'results2.json')
    sent = objecttosend.put(Body=result2json)