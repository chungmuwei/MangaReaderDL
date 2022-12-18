#!/usr/bin/env python3

import base64
import os
import time
import scrape
from sys import argv
from selenium import webdriver

def main():
    if len(argv) < 2:
        print('Usage: python run.py [manga_url]')
        return
    # Get the manga url from the second command line argument
    manga_url = argv[1]

    # webdriver settings
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Run Chrome in headless mode
    options.add_experimental_option('prefs', {
        "excludeSwitches": ["disable-popup-blocking"]
    })
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=options)
    # Load MangaReader.to page
    print("Loading MangaReader.to website...")
    driver.get(manga_url)
    
    # Click the vertical button to select vertical reading mode
    scrape.click_vertical_reading_mode_button(driver)
    time.sleep(1)
    window_name_ls = driver.window_handles
    driver.switch_to.window(window_name_ls[0])  # switch to the first window (mangareader.to)

    
    
    
    ### ORIGINAL METHOD: CANNOT DEAL WITH SHUFFLED IMAGE ###
    # Get all the links to the manga page images
    links = scrape.get_all_manga_pages_links(driver.page_source)
    if links is not None:
        print("Use original method to download the manga pages...")
        # Download and save all the images
        scrape.download_manga_pages(links, dirname= '_'.join(manga_url.split('/')[-3:]))
    else:
        print("Images were shuffled, use alternative method to download the manga pages...")
        # Wait for the page to load
        print("Loading manga page images...")
        scrape.wait_for_image_to_load(driver)

        # Get the base64 image
        base64_image_ls = get_base64_image(driver)
        print(f"Total pages found: {len(base64_image_ls)}")

        # Save the images
        print("Saving images...")
        save_images(base64_image_ls, dirname= '_'.join(manga_url.split('/')[-3:]))
        print("Done!")

def get_base64_image(driver):
    """
    Get the base64 image of all the canvas tags where the manga page images are stored
    """

    # Get the base64 image of all the canvas tags using querySelectorAll and toDataURL
    image_data_url_ls = driver.execute_script("""
        const canvasList = document.querySelectorAll('canvas');
        dataURLList = []
        for (let i = 0; i < canvasList.length; i++) {
            const canvas = canvasList[i];
            const dataURL = canvas.toDataURL('image/png').substring(21);
            dataURLList.push(dataURL);
        }
        return dataURLList;
    """)

    # Decode the base64 images
    base64_image_ls = []
    for image_data_url in image_data_url_ls:
        base64_image_ls.append(base64.b64decode(image_data_url))
    
    return base64_image_ls

def save_images(base64_image_ls, dirname=None):
    """
    Create a folder and save the base64 images png files
    """
    
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
    
    # Save all the images
    page_cnt = 1
    for base64_image in base64_image_ls:
        with open(dirname + '/page'+str(page_cnt) + '.png', 'wb') as f:
            f.write(base64_image) # write the base64 image to a file
        page_cnt += 1

if __name__ == '__main__':
    main()