import requests
from bs4 import BeautifulSoup

URL = 'https://liverpoolfc.com'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='featured-content')
match_elems = results.find_all('div', class_='matchinfo')

matches = []

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
  matches.append(
    {
      'home': home,
      'score': score,
      'away': away,
      'date': match_date.text.strip(),
      'comptetition': competition.replace('background-image: url(\'','').replace('\')', '')
    }
  )
print(matches)