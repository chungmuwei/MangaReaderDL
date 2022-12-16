# MangaReaderDL

A python web scraping script to download manga from [mangareader.to](http://mangareader.to/) using [serenium](), [bs4](), and [request]() libraries.

## Usage

1. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```
    or activate the virtual environment

    ```bash
    source MRDL-venv/bin/activate
    ```

1. Copy the url of the manga you want to download from [mangareader.to](http://mangareader.to/).

2.  Run the script with the url as an argument.

    ```bash
    python run.py <url>
    ```
3.  The script will create a folder with the name of the manga and download all the pages in it.