import json, glob, sys, requests
from bs4 import BeautifulSoup
from forge.downloader import get_data, download
root_uri = "http://files.minecraftforge.net"
ROOTPATH = "./data/forge"

print(sys.argv)
print(len(sys.argv))

if len(sys.argv) == 1:
    mainsoup = BeautifulSoup(requests.get(root_uri, allow_redirects=True).content, 'html.parser')
    for v in [a['href'] for a in mainsoup.find_all('a', href=True)]:
        if v.startswith("index_") and v.endswith(".html"):
            get_data(f"/maven/net/minecraftforge/forge/{v}")
else:
    for v in sys.argv:
        print(v)
        get_data("/maven/net/minecraftforge/forge/index_{}.html".format(v))

download(ROOTPATH)

with open(ROOTPATH + "/index.json", 'w') as f:
    index = [x.split('/')[-1].split('\\')[-1] for x in glob.glob("./../data/forge/*.zip")]
    f.write(json.dumps(index))