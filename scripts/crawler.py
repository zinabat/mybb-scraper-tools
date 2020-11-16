import asyncio
from lxml import html
import requests
import json
import time

session = requests.Session()
data = {
  'users': [],
  'threads': []
}
config = {
    "username": "Taikon",
    "password": "p00psc00p",
		"url":      "https://wolf-rpg.com/"
}
def login():
  postData = config.copy()
  postData['action'] = "do_login"
  postData['url'] = config['url'] + 'index.php'

  res = session.post(config['url'] + 'member.php', postData)
  # get users
  data['users'] = getUsers(html.fromstring(res.text))

def getUsers(tree):
  users = []
  userMenu = [el for el in tree.cssselect('.navbar .dropdown')][0]
  users.append({ 'username': userMenu.cssselect('.header-username')[0].text_content() })
  for el in userMenu.cssselect('.switchlink'):
    users.append({ 'username': el[0].text_content() })
  return users

def getThreads(username):
  postData = {
    "action": "do_search",
    "keywords": "",
    "postthread": 1,
    "author": username,
    "matchusername": 1,
    "forums[]": "all",
    "findthreadst": 1,
    "numreplies": "",
    "postdate": 0,
    "pddir": 1,
    "threadprefix[]": "any",
    "sortby": "lastpost",
    "sortordr": "desc",
    "showresults": "threads",
    "submit": "Search"
  }

  res = session.post(config['url'] + 'search.php', postData)

  # request next page if it exists until we're out of pages
  while True:
    tree = html.fromstring(res.text)
    # there's probably a better way to do fuzzy matching :/
    [processThreadRow(threadRow) for threadRow in tree.cssselect('.content-block .trow1')]
    [processThreadRow(threadRow) for threadRow in tree.cssselect('.content-block .trow2')]
    nextPage = tree.cssselect('.pagination_next')
    if len(nextPage) == 0:
      break
    res = session.get(config['url'] + nextPage[0].attrib['href'])

def processThreadRow(threadRow):
  icon = threadRow.cssselect('img')
  prefix = threadRow.cssselect('.prefix')
  subject = threadRow.cssselect('.subject_new')
  viewCount = None
  replyCount = None
  if len(subject) == 0:
    subject = threadRow.cssselect('.subject_old')
  extras = threadRow.cssselect('.col-xs-6 .col-sm-2')
  if len(extras) > 1:
    replyCount = extras[0].text_content().strip()
    viewCount = extras[1].text_content().strip()
  data['threads'].append({
    'href': subject[0].attrib['href'],
    'title': subject[0].text_content(),
    'prefix': prefix[0].text_content() if len(prefix) else None,
    'icon': icon[0].attrib['title'] if len(icon) else None,
    'viewCount': viewCount,
    'replyCount': replyCount
  })

login()
for user in data['users']:
  print('Fetching threads for user: ' + user['username'])
  getThreads(user['username'])
  time.sleep(30) # server limit
print(json.dumps(data, indent=4))
with open('data.txt', 'w') as outfile:
  json.dump(data, outfile, indent=2)