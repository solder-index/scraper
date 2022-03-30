from datetime import datetime, timedelta
import requests
import json
import dateutil.parser

from multiprocessing import Pool
import hashlib
import zipfile
import os.path
import os
import glob
import json
import pytz

from curseforge_api.client import HttpClient

BASE_URI = "https://addons-ecs.forgesvc.net/api/v2/addon"

def get_list(ID):
    json_file = HttpClient.get("{}/{}/files".format(BASE_URI, ID))
    print(json_file)
    return json.loads(json_file.content)
    
def get_modloader(i, single_name) -> str:
    if single_name:
        return ""
    if "Forge" in i["gameVersion"] or "forge" in i["url"].lower():
        "-forge"
    if "Fabric" in i["gameVersion"] or "fabric" in i["url"].lower():
        "-fabric"
    return ""

def is_old(x):
    return dateutil.parser.parse(x["fileDate"]).replace(tzinfo=pytz.UTC) > (datetime.now(pytz.UTC) - timedelta(days=400))

def get_download_uri(addon, file):
    return HttpClient.get(f"{BASE_URI}/{addon}/file/{file}/download-url")

def get_file_md5(addon, file):
    return HttpClient.get(f"{BASE_URI}/{addon}/file/{file}/download-url")

def get_download_list(addonId):
    return [{ "url": x["downloadUrl"], "gameVersion": x["gameVersion"]} for x in get_list(addonId) if is_old(x)]

def get_alternate_download_list(addonId):
    return [{ "url": get_download_uri(addonId, x["alternateFileId"]), "gameVersion": x["gameVersion"]} for x in get_list(addonId) if is_old(x)]

def get_info(ID):
    json_file = HttpClient.get("{}/{}".format(BASE_URI, ID))
    return json.loads(json_file.content)
