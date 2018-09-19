#!/usr/bin/python3
from urllib.parse import urlparse
import requests

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Fetch a github repo's commit list.")
    parser.add_argument(dest='url', type=str, help='the url of the github repo')
    args = parser.parse_args()

    url_parts = urlparse(args.url)
    print(url_parts)
    if not all([url_parts.scheme, url_parts.netloc, url_parts.path]):
        raise ValueError('Invalid url, please double check it.')

    response = requests.get(f'https://api.github.com/repos{url_parts.path}/commits')
    print(response.content)
