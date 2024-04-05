import requests
from bs4 import BeautifulSoup
import logging
import urllib3
import os

urllib3.disable_warnings()
base_url = "https://network.satnogs.org/observations/"
observation_url = "https://network.satnogs.org/observations/"
logging.basicConfig(level=logging.INFO)
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
}

proxies = {"http": 'http://127.0.0.1:7890', 'https': 'https://127.0.0.1:7890'}
for i in range(78):
    r = requests.get(
        base_url + f"?future=0&bad=0&unknown=0&failed=0&norad=&start=2024-04-04+00%3A00&end=2024-04-05+00%3A00&observer=&station=&transmitter_mode=&transmitter_uuid=&page={i + 1}",
        verify=False, headers=headers)
    print("Status Code: ", r.status_code, end="\t")
    if r.status_code != 200:
        print(f"Error when access page {i + 1}, continue access next page!")
        continue
    else:
        print(f"Success access page {i + 1}!")
        soup_total = BeautifulSoup(r.text, 'html.parser')
        trs = soup_total.find_all(class_="clickable-row")
        # print(trs)
        for tr in trs:
            current_id = tr['data-href'].split('/')[-2]
            # print(current_id)
            new_url = base_url + current_id
            if os.path.exists(f"./results/{current_id}"):
                continue
            os.mkdir(f"./results/{current_id}")
            print(f"id: {current_id}")
            r = requests.get(new_url, verify=False, headers=headers)
            if r.status_code != 200:
                print(f"Failed to access id {current_id}, continue access next id!")
                continue
            else:
                soup = BeautifulSoup(r.text, 'html.parser')
                div_nodes = soup.find('table', class_='table table-sm table-borderless table-hover')
                trs = div_nodes.find_all('tr')
                fs = open(f"./results/{current_id}/basic_info.txt", "a")
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
                    r = requests.get(water_url, verify=False, headers=headers)
                    with open(f"./results/{current_id}/{waterfall_id}.png", 'wb') as f:
                        f.write(r.content)
                    r.close()
                audio = soup.find(id="tab-audio")
                if audio.find('div', class_="wave tab-data") is not None:
                    audio_url = audio.find('div', class_="wave tab-data")['data-audio']
                    audio_id = audio.find('div', class_="wave tab-data")['id']
                    # print(audio_url)
                    r = requests.get(audio_url, verify=False, headers=headers)
                    with open(f"./results/{current_id}/{audio_id}.ogg", 'wb') as f:
                        f.write(r.content)
                    r.close()
                data = soup.find(id="tab-data")
                infos = data.find_all('div', class_="demoddata")
                if infos is not None:
                    for info in infos:
                        info_url = info.find('a')['href']
                        name = info.find('a').get_text().strip().split('/')
                        data_name = name[-1]
                        # print(data_name)
                        r = requests.get(info_url, verify=False, headers=headers)
                        with open(f"./results/{current_id}/{data_name}.dat", "wb") as f:
                            f.write(r.content)
                        r.close()
            print(f"Finish: {current_id}")
            r.close()
    r.close()
