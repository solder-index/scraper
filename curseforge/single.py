from multiprocessing import Pool
import hashlib
import zipfile
import os.path
import os
import glob
import json
from . import DOWNLOAD_PATH

from curseforge_api.api import get_download_list, get_info, get_modloader
from curseforge_api.client import HttpClient


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def process(data, mod_name, single_name):
    name = data["url"].split('/')[-1]
    dataPath = "{}/{}{}/{}".format(DOWNLOAD_PATH, mod_name, get_modloader(data, single_name), name)
    folderPath = "{}/{}{}".format(DOWNLOAD_PATH, mod_name, get_modloader(data, single_name))
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    print(dataPath)
    print(name)
    if os.path.isfile(dataPath.replace(".jar", ".zip")) is False:
        try:
            r = HttpClient.get(data["url"])
            with open(name, 'wb') as f:
                f.write(r.content)
            with zipfile.ZipFile(dataPath.replace(".jar", ".zip"), 'a') as zipf:
                destination = 'mod/' + name
                zipf.write(name, destination)
            f = open(dataPath.replace(".jar", ".md5"), "a")
            f.write(md5(dataPath.replace(".jar", ".zip")))
            f.close()
            os.remove(name)
        except Exception as ex:
            print(f"failed {ex}")
    else:
        print("skiped")

def start():

    with open('curseforge/single.json') as json_file:
        data = json.load(json_file)
        for mod in data: 
            for i in get_download_list(mod["id"]):
                process(i, mod["name"], mod.get("single_name", False))
            with open("{}/{}/index.json".format(DOWNLOAD_PATH, mod["name"]), 'w') as f:
                mod_data = get_info(mod["id"])
                file_data = {
                    "files": [x.split('/')[-1].split('\\')[-1] for x in glob.glob("{}/{}/*.zip".format(DOWNLOAD_PATH, mod["name"]))],
                    "websiteUrl": mod_data["websiteUrl"],
                    "description": mod_data["summary"],
                    "author": ", ".join(x["name"] for x in mod_data["authors"])
                }
                f.write(json.dumps(file_data))