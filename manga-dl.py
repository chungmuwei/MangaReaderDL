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
    options.add_argument('--headless') # Run Chrome in headless mode
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
    # Get all the manga page image byte strings
    base64_image_ls = scrape.get_all_manga_pages_image(driver.page_source)

    save_images(driver, base64_image_ls, dirname= '_'.join(manga_url.split('/')[-3:]))

    '''
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
    '''

def get_base64_image(driver, page_number: int):
    """
    Get the base64 image of all the canvas tags where the manga page images are stored
    """

    # Get the base64 image of all the canvas tags using querySelectorAll and toDataURL
    image_data_url = driver.execute_script("""
        const pageNumber = arguments[0];
        const canvas = document.querySelector(`#vertical-content > div:nth-child(${pageNumber}) > canvas`);
        dataURL = canvas.toDataURL('image/png').substring(21);
        return dataURL;
    """, page_number)

    # Decode the base64 image
    base64_image = base64.b64decode(image_data_url)
    
    return base64_image

def save_images(driver, base64_image_ls, dirname=None):
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
        sequence_cnt += 1
    os.makedirs(dirname, exist_ok=False)
    
    # Save all the images
    page_cnt = 1
    first_none_page = True
    for base64_image in base64_image_ls:

        if base64_image == None:

            if first_none_page:
                scrape.wait_for_image_to_load(driver)
                first_none_page = False

            base64_image = get_base64_image(driver, page_cnt)

        with open(dirname + '/page'+str(page_cnt) + '.png', 'wb') as f:
            f.write(base64_image) # write the base64 image to a file
        page_cnt += 1

if __name__ == '__main__':
    main()