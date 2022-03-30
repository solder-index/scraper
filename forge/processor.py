from multiprocessing import Pool
import hashlib
import zipfile
import os.path
import os
import glob
import json

ROOTPATH = "./../data/forge/"

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def _process(filepath):
    if os.path.isfile(filepath.replace(".jar", ".zip")) is False:
        with zipfile.ZipFile(filepath.replace(".jar", ".zip"), 'a') as zipf:
            destination = 'bin/modpack.jar'
            zipf.write(filepath, destination)
        f = open(filepath.replace(".jar", ".md5"), "a")
        f.write(md5(filepath.replace(".jar", ".zip")))
        f.close()
    os.remove(filepath)
        

for i in glob.glob("{0}*.jar".format(ROOTPATH)):
    _process(i)

with open(ROOTPATH + "index.json", 'w') as f:
    index = [x.split('/')[-1].split('\\')[-1] for x in glob.glob("./../data/forge/*.zip")]
    f.write(json.dumps(index))