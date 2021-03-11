import requests
from bs4 import BeautifulSoup
import json, codecs
import os
from git import Repo
import urllib.request
from datetime import datetime

now = datetime.now()
 
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

URL = 'https://liverpoolfc.com'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='featured-content')
match_elems = results.find_all('div', class_='matchinfo')

data = {}
i = 0
for elem in match_elems:
  teams = elem.find_all('img', class_='badge')
  home = teams[0]['src']
  away = teams[1]['src']
  score = elem.find('span', class_='score')
  if score == None:
    score = 'v'
  else:
    score = score.text
  match_date = elem.find('p')
  competition = elem.find('div', class_='comp-logo')['style']
  
  data[i] = {
    'home': home,
    'score': score,
    'away': away,
    'date': match_date.text.strip(),
    'competition': competition.replace('background-image: url(\'','').replace('\')', '')
  }
  i+=1
  
types = ['last', 'current', 'next']

for i in data:
  urllib.request.urlretrieve(data[i]['home'], '/media/pi/NAS/Jake/Development/liverpool-matches/' + types[i] + '/home-team.png')
  urllib.request.urlretrieve(data[i]['away'], '/media/pi/NAS/Jake/Development/liverpool-matches/' + types[i] + '/away-team.png')
  urllib.request.urlretrieve(data[i]['competition'], '/media/pi/NAS/Jake/Development/liverpool-matches/' + types[i] + '/competition.png')
  with open('/media/pi/NAS/Jake/Development/liverpool-matches/' + types[i] + "-match.json", "w") as write_file:
    json.dump(data[i], write_file)
  

repo_dir = '/media/pi/NAS/Jake/Development/liverpool-matches/'
repo = Repo(repo_dir)

file_list = [
  'liverpool.py',
  'last-match.json', 
  'current-match.json', 
  'next-match.json', 
  'last/home-team.png', 
  'last/away-team.png', 
  'last/competition.png', 
  'current/home-team.png', 
  'current/away-team.png', 
  'current/competition.png', 
  'next/home-team.png', 
  'next/away-team.png', 
  'next/competition.png'
]

commit_message = 'Updated: ' + dt_string
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()