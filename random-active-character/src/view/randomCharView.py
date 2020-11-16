import requests

def lambda_handler(event, context):
  with open("random-character.html", "r") as file:
    data = file.read()
  return {
    "statusCode": 200,
    "body": data,
    "headers": {
        'Content-Type': 'text/html',
    }
  }