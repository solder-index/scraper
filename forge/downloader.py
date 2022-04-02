from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import os.path
import sys
import hashlib
import zipfile

import json

root_uri = "http://files.minecraftforge.net"
to_download = []
to_download_total = 0

def get_data(v):
    global to_download
    print(root_uri + v)
    soup = BeautifulSoup(requests.get(root_uri + v, allow_redirects=True).content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    for link in links:
        if link.startswith("https://maven.minecraftforge.net/") and link.endswith("universal.jar"):
            to_download.append(link)
            print(f"\nusing {link}\n")

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def process(filepath):
    if os.path.isfile(filepath.replace(".jar", ".zip")) is False:
        with zipfile.ZipFile(filepath.replace(".jar", ".zip"), 'a') as zipf:
            destination = 'bin/modpack.jar'
            zipf.write(filepath, destination)
        f = open(filepath.replace(".jar", ".md5"), "a")
        f.write(md5(filepath.replace(".jar", ".zip")))
        f.close()
    os.remove(filepath)


def download(download_path):
    print("downloading")
    global to_download
    global to_download_total
    to_download = list(set(to_download))
    to_download_total = len(to_download)
    for i in to_download:
        download_item(download_path, i)

def download_item(download_path, i):
    global to_download
    global to_download_total
    file_path = "{}/{}".format(download_path, i.split('/')[-1].replace("-universal", ""))
    if os.path.isfile(file_path) is False:
        r = requests.get(i)
        with open(file_path, 'wb') as f:
            f.write(r.content)
        process(file_path)
    print(f"{len(to_download) - to_download_total}/{to_download_total}")

