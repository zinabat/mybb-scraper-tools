import json
import webbrowser
import random
import os
from lxml import html
import requests

POST_MIN = int(os.environ['POST_MIN'], 10)

def getCachedUsers():
  with open('activeUsers.json', 'r') as infile:
    users = json.load(infile)
    return users

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

def generateRandomChar():
  users = getCachedUsers()
  filtered = list(filter(isNominableUser, users))
  print('Choosing from ' + str(len(filtered)) + ' characters with >= ' + str(POST_MIN) + ' posts and not "PPC"')
  return random.choice(filtered)

def makeCotMTemplate(user):
  imgUrl = getAvatar(user)
  img = '[img]'+imgUrl+'[/img]' if imgUrl else ''
  template = '''
<!DOCTYPE html>
<html>
<head>
  <style>
    div.wrapper {{
      width: 500px;
      margin: 0 auto;
      padding: 50px 0;
    }}
    code {{
      border: 1px solid #5e96db;
      display: block;
      padding: 5px;
      background: #0b1520;
      color: #ffdca5;
    }}
  </style>
</head>
<body>
<div class="wrapper">
  <h2>Random Active Character</h2>
  <p>This character was randomly picked from non PPC characters with >= {postMin} posts.</p>
  <div style="text-align: center">
    <img src="{imgUrl}" alt="">
    <h3><a href="{url}" target="_blank">{name}</a></h3>
  </div>
  <h2>Character of the Month Code</h2>
  <code>
    [narrow][border][align=center][h1]Character of the Month[/h1]
    {img}
    [h2][url={url}]{name}[/url][/h2]
    [hr]
    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
    [small]This character was pulled from a virtual hat![/small]
    [/align][/border][/narrow]
  </code>
</div>
</body>
</html>
  '''.format(img = img, imgUrl = imgUrl, url=user['href'], name=user['name'], postMin=POST_MIN)
  filename = ''
  with open('random-character.html', 'w') as outfile:
    outfile.write(template)
    filename = outfile.name
  webbrowser.open('file://' + os.path.realpath(filename))

user = generateRandomChar()
makeCotMTemplate(user)