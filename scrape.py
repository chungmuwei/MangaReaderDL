import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time

def get_html(url):
    r = requests.get(url)
    return r.text

def click_vertical_reading_mode_button(driver):
    # Get the vertical reading mode button
    button = driver.find_element(By.XPATH, '//*[@id="first-read"]/div[1]/div/div[3]/a[1]')
    # Click the button
    button.click()

def get_vertical_content_container(html):
    """
    Helper function for get_all_manga_pages_links.\n
    Return the manga page container.
    """
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find('div', id='vertical-content')
    return container
    
def get_all_manga_pages_links(html):
    container = get_vertical_content_container(html)
    pages = container.find_all('div')
    links = []
    for page in pages:
        link = page.get('data-url')
        if link is not None:
            if 'shuffled' in page['class']: 
                return None
            else:
                links.append(link)
    return links

def wait_for_image_to_load(driver):
    time.sleep(1)   #TODO: Find a better way to wait for the page to load
   
    # Scroll down to view all image one by one to load all the images
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    # driver.execute_script("window.scrollTo(0, {});".format(total_height))
    # print("initial total_height: {}".format(total_height))
    current_height = 0
    interval = 50
    while current_height < total_height:
        driver.execute_script("window.scrollTo(0, {});".format(current_height))
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        current_height += interval
        time.sleep(0.01)
        # if current_height % 1000 == 0:
        #     print("{}-th iteration current_height: {}, total_height: {}".format(current_height//interval, current_height, total_height))
    time.sleep(1)


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