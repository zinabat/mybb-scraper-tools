import boto3
import json
import random
import os
from lxml import html
import requests

POST_MIN = int(os.environ['POST_MIN'], 10)

def lambda_handler(event, context):
    #fetch from s3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='wolfrpg-characters', Key='active-chars.json')
    users = json.loads(obj['Body'].read().decode('utf-8'))

    user = generateRandomChar(users)
    user['img'] = getAvatar(user)

    return {
        "statusCode": 200,
        "body": json.dumps(user),
    }

def isNominableUser(user):
    if int(user['postCount']) < 50:
        return False
    if 'rank' in user and user['rank'] == 'PPC':
        return False
    return True

def getAvatar(user):
    res = requests.get(user['href'])
    root = html.fromstring(res.text)
    imgs = root.cssselect('.profile-block img')
    # get the first image - this is usually the avatar
    if len(imgs):
        return imgs[0].attrib['src']
    return None

def generateRandomChar(users):
    filtered = list(filter(isNominableUser, users))
    return random.choice(filtered)

