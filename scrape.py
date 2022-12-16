import requests
from bs4 import BeautifulSoup
import os
import time

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_manga_pages_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find('div', id='vertical-content')
    pages = container.find_all('div')
    links = []
    for page in pages:
        link = page.get('data-url')
        if link is not None:
            links.append(link)
    return links

def download_manga_pages(links, dirname=None):
    # Create a new directory with the current date and time
    if dirname is None:
        dirname = time.strftime('%Y-%m-%d_%H-%M-%S')
    sequence_cnt = 1
    # If the directory already exists, create a new one with a sequence number
    while os.path.exists(dirname):
        if sequence_cnt > 1:
            dirname = dirname.rstrip('_' + str(sequence_cnt - 1))
        dirname = dirname + '_' + str(sequence_cnt)
    os.makedirs(dirname, exist_ok=False)
    # Download and save all the images
    page_cnt = 1
    for link in links:
        img = requests.get(link).content
        with open(dirname + '/page'+str(page_cnt) + '.jpg', 'wb') as handler:
            handler.write(img)
        page_cnt += 1