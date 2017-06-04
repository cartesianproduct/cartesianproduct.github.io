
__auther__ = "Baolin liu"

import boto.dynamodb
import json
import datetime
import ast
import simplejson as j

"""

Insert info into Dynamodb and ways to view info by pcode

http://boto.cloudhackers.com/en/latest/dynamodb_tut.html
http://boto.cloudhackers.com/en/latest/ref/dynamodb.html

"""


f = open("rootkey.json")
data = json.load(f) 
aws_access_key_id = data['AWSAccessKeyId'] 
aws_secret_access_key = data['AWSSecretKey']
region_name = data['region_name']

c = boto.dynamodb.connect_to_region(aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key,
                                    region_name=region_name)

table = c.get_table("MyanmarCP")


# add features here from Google Sheets
Name = j.dumps('string123katie')
PCode = j.dumps('string')
Census = j.dumps([1334])
Geography = j.dumps(["polygons"])
User_Input =  j.dumps('user input')
ReceivedTime =  datetime.datetime.now().strftime("%d %B %Y %I:%M%p")
 
# use ast.literal_eval(string value) to get the data out of stringify setup

item_data = {
        'Name': Name,
        'PCode': PCode,
        'Census': Census,
        'Geography': Geography,
        'User Input': User_Input,
        'ReceivedTime': ReceivedTime 
    }


item = table.new_item(
        hash_key=PCode,
        range_key=None,
        attrs=item_data
    )

item.put()
