import logging
import os
from pathlib import Path

import feedparser
import requests

feed_url = "https://musicforprogramming.net/rss.xml"

etag_file = "musicforprogramming.etag"

logger = logging.getLogger(__name__)


def get_etag():

    p = Path(data_path) / etag_file
    if not p.exists():
        return None
    with p.open("r") as fh:
        return fh.read()


def save_etag(etag: str):

    p = Path(data_path) / etag_file
    if not p.exists():
        p.touch()
    p.write_text(etag)


def get_filename(full_link: str):
    origin_name = full_link.split("music_for_programming_")[1]
    n = origin_name.split("-")
    serial = int(n[0])
    return '-'.join((f'{serial:03d}',*n[1:]))


def download():
    d = feedparser.parse(feed_url, get_etag())
    # print(d.keys())
    print(d.etag)
    # feed = d.feed
    # print(type(feed))
    # print(feed.keys())
    for item in d.entries:
        file_url = item.id
        f = Path(data_path) / get_filename(file_url)

        if not f.exists():
            with requests.get(file_url, stream=True) as resp:
                if resp.status_code != 200:
                    logger.error(resp.content)
                else:
                    logger.info(f"start to download {f}")
                    totalbits = 0
                   
                    with f.open("wb") as fh:
                        for chunk in resp.iter_content(chunk_size=1024):
                            if chunk:
                                totalbits += 1024
                                fh.write(chunk)
                    logger.info(f"{f} download finished in {totalbits}")
        else:
            logger.info(f"{f} already exists")
        
    # save_etag(d.etag)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    data_path = os.getenv('DATA_PATH', "/data/music")
    logger.info(f"start to download to {data_path}")
    download()
