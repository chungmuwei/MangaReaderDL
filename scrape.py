import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import os
import time

def get_html(url):
    r = requests.get(url)
    return r.text

def click_vertical_reading_mode_button(driver):

    # Get the vertical reading mode button 
    # FULL XPATH: '//*[@id="first-read"]/div[1]/div/div[3]/a[1]' 
    # XPATH:      '//*[@id="first-read"]/div[1]/div/div[3]/a[1]'
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[1]/div/div[3]/a[1]')
    # Click the button
    # button.click()
    
    # 6 March 2023
    # website seems to have changed, the above code no longer works
    # need to click the button twice
    ActionChains(driver).move_to_element(button).click().perform();
    ActionChains(driver).move_to_element(button).click().perform();


def get_vertical_content_container(html):
    """
    Helper function for get_all_manga_pages_links.\n
    Return the manga page container.
    """
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find('div', id='vertical-content')
    return container
    
def get_all_manga_pages_image(html):
    """
    :param html: the html of the manga reading page\n
    :return: a list of byte strings representing manga page images\n

    Find all div tags with class "iv-card". If the manga page image is not shuffled, 
    the link to the image is stored in the "data-url" attribute. So the byte string of the image 
    can be obtained by sending a GET request to the link. If the manga page image is shuffled, 
    just append None to the list and use alternative method the obtained it later.
    """

    container = get_vertical_content_container(html)
    pages = container.find_all(name='div', attrs={'class': 'iv-card'})
    base64_image_ls = []
    normal_image_count = 0
    shuffled_image_count = 0
    # Iterate through all the pages
    for page in pages:
        # Append None to the list if the page is shuffled
        if 'shuffled' in page['class']:
            base64_image_ls.append(None)
            shuffled_image_count += 1
            continue

        # Get the link to the image
        link = page.get('data-url')
        # Append the link to the list if it is not None
        if link is not None:
            base64_image = requests.get(link).content # type: bytes
            base64_image_ls.append(base64_image)
            normal_image_count += 1

    return base64_image_ls, normal_image_count, shuffled_image_count

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
        print("\rScrolling down to load images: current height: {}, total height: {}".format(current_height, total_height), end='')
    time.sleep(max(3, total_height/50000))


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