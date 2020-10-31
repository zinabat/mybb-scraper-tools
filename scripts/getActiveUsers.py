import asyncio
from lxml import html
import requests
import json
import time
import os

config = {
  "url": os.environ["URL"],
  "waitTime": int(os.environ['WAIT_TIME'], 10)
}

# get pack/group links from stats page
def getGroups():
  res = requests.get(config['url'] + 'stats.php')
  root = html.fromstring(res.text)
  links = root.cssselect('.trow1 a')
  links.extend(root.cssselect('.trow2 a'))
  return [link.attrib['href'] for link in links]

# for each group link, get users
async def getGroupUsers(groupLink):
  res = requests.get(config['url'] + groupLink)
  users = []
  pageCount = 0
  url = config['url'] + groupLink
  while True:
    pageCount += 1
    print('Page: ' + str(pageCount))

    res = requests.get(url)
    # todo: on failure
    root = html.fromstring(res.text)
    rows = root.cssselect('.rankrow')
    for row in rows:
      link = row.cssselect('div a')
      if len(link):
        link = link[0]
      else:
        continue
      user = { 'href': link.attrib['href'], 'name': link.text_content() }
      rank = row.cssselect('.col-xs-4')
      if len(rank):
        user['rank'] = rank[0].text_content().strip()
      user['postCount'] = row.cssselect('div')[-1].cssselect('span')[0].text_content().strip()
      users.append(user)
    nextPage = root.cssselect('.pagination_next')
    if len(nextPage):
      url = config['url'] + nextPage[0].attrib['href']
    else:
      break
  return users

async def main():
  groupLinks = getGroups()
  users = []
  for groupLink in groupLinks:
    print('Gathering from: ' + groupLink)
    theseUsers = await getGroupUsers(groupLink)
    print([user for user in theseUsers])
    users.extend(theseUsers)
    print('Waiting...')
    time.sleep(config['waitTime'])
  with open('activeUsers.json', 'w') as outfile:
    json.dump(users, outfile, indent=2)
  print('Write complete.')

asyncio.run(main())