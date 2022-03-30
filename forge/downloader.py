from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import os.path
import sys

import json

root_uri = "http://files.minecraftforge.net"
to_download = []

def get_data(v):
    global to_download
    print(root_uri + v)
    soup = BeautifulSoup(requests.get(root_uri + v, allow_redirects=True).content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    for link in links:
        if link.startswith("/maven/net/minecraftforge/forge") and link.endswith("universal.jar"):
            to_download.append(link)
            print(link)

def download():
    global to_download
    to_download = list(set(to_download))
    done = 0
    todo = len(to_download)
    for i in to_download:
        if os.path.isfile(i.split('/')[-1]) is False:
            r = requests.get(root_uri + i)
            with open("../data/forge/{}".format(i.split('/')[-1].replace("-universal", "")), 'wb') as f:
                f.write(r.content)
        done = done + 1
        print("{}/{}".format(done, todo))
        
print(sys.argv)
print(len(sys.argv))

if len(sys.argv) == 1:
    mainsoup = BeautifulSoup(requests.get(root_uri, allow_redirects=True).content, 'html.parser')
    for v in [a['href'] for a in mainsoup.find_all('a', href=True)]:
        if v.startswith("/maven/net/minecraftforge/forge/index_") and v.endswith(".html"):
            get_data(v)
else:
    for v in sys.argv:
        print(v)
        get_data("/maven/net/minecraftforge/forge/index_{}.html".format(v))


download()
print("DONE")