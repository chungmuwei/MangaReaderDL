# MangaReaderDL

A python web scraping script to download manga from [mangareader.to](http://mangareader.to/) using [Selenium](https://pypi.org/project/selenium/), [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), and [requests](https://pypi.org/project/requests/) libraries.

## Usage

You can either run the standalone executable packaged by [PyInstaller](https://pypi.org/project/pyinstaller/) or run the script directly.

### Run the standalone executable

>  ⚠️ Notice: It is only compatible with **Mac OS X**. The 
> windows and Linux version will be released soon.

1. The executable is located in the `dist` folder. You can run it by from the project root directory.

```bash
./dist/manga-dl <url>
```
or double click on the executable file in Finder.

### Run the script directly

1. Activate the virtual environment by

    ```bash
    source venv/bin/activate
    ```
    
    then install the dependencies by

    ```bash
    pip install -r requirements.txt
    ```

2. Copy the url of the manga you want to download from [mangareader.to](http://mangareader.to/). E.g., you wanted to download Chainsaw Man Chapter 1 in English, then copy the url https://mangareader.to/read/chainsaw-man-96/en/chapter-1

3.  Run the script and input the url.

    ```bash
    python manga-dl.py 
    ```
    Below are the output of this example.
    ```
    1.Paste the url of the manga chapter/volume from MangaReader website: 
    https://mangareader.to/read/chainsaw-man-96/en/chapter-1

    Done loading website ✅

    2. Scraping normal manga page images...
    Total pages found: 53
    Normal pages found: 0
    Shuffled pages found: 53
    Done scraping normal pages ✅

    3. Scraping shuffled manga page image and save image...
    Created directory: chainsaw-man-96_en_chapter-1 to save the manga images
    Saving images: 54 pages saved in chainsaw-man-96_en_chapter-1 directory
    Done saving images ✅
    ```
4.  The script will create a folder with the name of the manga, download all the pages and save each page as a PNG file.

## Implementations

1.  The script uses [Selenium](https://pypi.org/project/selenium/) instantiate a **Chrome webdriver** to open the manga page in a headless browser (run in background).
2.  It is required to **select the reading mode** before reading manga for the first read. There are two options, **Vertical Follow** and **Horizontal Follow**. For my implementation, the webdriver will then find **Vertical Follow** button by its XPATH and **click** it in order to display manga image.
3. Most images except those belonged to newly released chapters are located in `canvas` tag which has a url in the `data-url` attribute linking to a **shuffled** image. They are dynamically restored and loaded by JavaScript. Below is a shuffled image of the [Attack on Titan](https://en.wikipedia.org/wiki/Attack_on_Titan) Manga Volume 1 cover:

<img align="center" src="https://c-1.mreadercdn.com/_v2/0/0dcb8f9eaacfd940603bd75c7c152919c72e45517dcfb1087df215e3be94206cfdf45f64815888ea0749af4c0ae5636fabea0abab8c2e938ab3ad7367e9bfa52/52/f3/52f3b6d9ac0123042cebb6fd7839fda6/52f3b6d9ac0123042cebb6fd7839fda6_1900.jpeg?t=515363393022bbd440b0b7d9918f291a&ttl=1908547557" height=300 />

