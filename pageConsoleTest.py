import requests
from bs4 import BeautifulSoup
import logging
import urllib3
import os

urllib3.disable_warnings()
base_url = "https://network.satnogs.org/observations/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
}
for i in range(1):
    r = requests.get(base_url + f"?future=0&bad=0&unknown=0&failed=0&norad=&start=2024-04-04+07%3A46&end=&observer=&station=&transmitter_mode=&transmitter_uuid=&page={i + 1}", verify=False, headers=headers)
    print(r.status_code)
    if r.status_code != 200:
        logging.error(f"Error when access page {i + 1}, continue access next page!")
        continue
    else:
        logging.info(f"Success access page {i + 1}!")
        soup_total = BeautifulSoup(r.text, 'html.parser')
        trs = soup_total.find_all(class_="clickable-row")
        # print(trs)
        for tr in trs:
            current_id = tr['data-href'].split('/')[-2]
            print(current_id)
            new_url = base_url + current_id
            # os.mkdir(f"./results/{current_id}")
            logging.info(f"id: {current_id}")