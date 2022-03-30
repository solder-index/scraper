from requests import Session


__headers = {
    'User-Agent': 'Solder-index 1.0'
}

HttpClient = Session()
HttpClient.headers.update(__headers)