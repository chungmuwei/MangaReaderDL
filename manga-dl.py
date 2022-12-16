#!/usr/bin/env python3

import scrape
from sys import argv
from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    if len(argv) < 2:
        print('Usage: python run.py [manga_url]')
        return
    # Get the manga url from the command line
    manga_url = argv[1]
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    # Load MangaReader.to page
    driver.get(manga_url)
    # Click the vertical button to select vertical reading mode
    button = driver.find_element(By.XPATH, '//*[@id="first-read"]/div[1]/div/div[3]/a[1]')
    # print(button.text)
    button.click()

    # Get all the links to the manga page images
    links = scrape.get_all_manga_pages_links(driver.page_source)
    # Download and save all the images
    scrape.download_manga_pages(links, dirname= '_'.join(manga_url.split('/')[-3:]))

if __name__ == '__main__':
    main()