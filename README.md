# MangaReaderDL

A python web scraping script to download manga from [mangareader.to](http://mangareader.to/) using [Selenium](https://pypi.org/project/selenium/), [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), and [requests](https://pypi.org/project/requests/) libraries.

## Usage

You can either run the standalone executable packaged by [PyInstaller](https://pypi.org/project/pyinstaller/) or run the script directly.

### Run the standalone executable

1. The executable is located in the `dist` folder. You can run it by

```bash
./dist/manga-dl <url>
```

### Run the script directly

1. Activate the virtual environment by

    ```bash
    source MRDL-venv/bin/activate
    ```
    
    then install the dependencies by

    ```bash
    pip install -r requirements.txt
    ```

2. Copy the url of the manga you want to download from [mangareader.to](http://mangareader.to/). E.g., you wanted to download Chainsaw Man Chapter 1 in English, then copy the url https://mangareader.to/read/chainsaw-man-96/en/chapter-1

3.  Run the script with the url as an argument. 

    ```bash
    python run.py https://mangareader.to/read/chainsaw-man-96/en/chapter-1
    ```
4.  The script will create a folder with the name of the manga, download all the pages and save each page as a PNG file.

## Implementations

1.  The script uses [Selenium](https://pypi.org/project/selenium/) instantiate a **Chrome webdriver** to open the manga page in a headless browser (run in background).
2.  It is required to **select the reading mode** before reading manga for the first read. There are two options, **Vertical Follow** and **Horizontal Follow**. For my implementation, the webdriver will then find **Vertical Follow** button by its XPATH and **click** it in order to display manga image.
3. TBC