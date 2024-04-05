import requests
from bs4 import BeautifulSoup

import os

url = "https://network.satnogs.org/observations/9313125/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
div_nodes = soup.find('table', class_='table table-sm table-borderless table-hover')
trs = div_nodes.find_all('tr')
os.mkdir(f"./results/{9313125}")
fs = open(f"./results/{9313125}/basic_info.txt", "a")
for tri in trs:
    tds = tri.find_all('td')
    if len(tds) == 0:
        continue
    a = tds[0].get_text().strip()
    if a == "Polar Plot":
        continue
    if a == "Downloads":
        continue
    print(f"{a}: ", end="", file=fs)
    print(tds[1].get_text().replace('\n', ' ').strip(), file=fs)
    fs.flush()
fs.close()

waterfall = soup.find('div', id="tab-waterfall")

if waterfall.find('img') is not None:
    waterfall_id = waterfall.find('img').parent['id']
    water_url = waterfall.find('img')['src']
    r = requests.get(water_url)
    with open(f"./results/{9313125}/{waterfall_id}.png", 'wb') as f:
        f.write(r.content)
audio = soup.find(id="tab-audio")
if audio.find('div', class_="wave tab-data") is not None:
    audio_url = audio.find('div', class_="wave tab-data")['data-audio']
    audio_id = audio.find('div', class_="wave tab-data")['id']
    print(audio_url)
    r = requests.get(audio_url)
    with open(f"./results/{9313125}/{audio_id}.ogg", 'wb') as f:
        f.write(r.content)

data = soup.find(id="tab-data")
infos = data.find_all('div', class_="demoddata")
if infos is not None:
    for info in infos:
        info_url = info.find('a')['href']
        name = info.find('a').get_text().strip().split('/')
        data_name = name[-1]
        print(data_name)
        r = requests.get(info_url)
        with open(f"./results/{9313125}/{data_name}.dat", "wb") as f:
            f.write(r.content)
