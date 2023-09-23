# MangaReaderDL

A python web scraping script to download manga from [mangareader.to](http://mangareader.to/) using [Selenium](https://pypi.org/project/selenium/), [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), and [requests](https://pypi.org/project/requests/) libraries.

## Usage

You can either run the standalone executable packaged by [PyInstaller](https://pypi.org/project/pyinstaller/) or run the script directly.

### Install the package

- Use `pip` to install the package

    ```bash
    pip install dist/manga-dl-0.3.0.tar.gz
    ```

### Run the Python file directly

1. Create a python3.11 virtual environment by

    ```bash
    virtualenv venv --python=python3.11
    ```

2. Activate the virtual environment by

    ```bash
    source venv/bin/activate
    ```
    
    then install the dependencies by

    ```bash
    pip install -r requirements.txt
    ```

### Usage

> `manga-dl.py [OPTIONS] ✨Manga URL✨ ✨Save Path✨`

1. Go to [mangareader.to](http://mangareader.to/) and copy the URL of the manga you want to download. The URL pattern should be `https://mangareader.to/read/<manga-name>/<language>/<chapter/volume>`

2.  Run `python3 app/manga-dl.py <URL> [PATH]` to download the manga and save it in path. If path is not specified, the manga will be saved in the current directory.

3. You can run `python3 app/manga-dl.py --help` to see the help message.

## Implementations

1.  The script uses [Selenium](https://pypi.org/project/selenium/) instantiate a **Chrome webdriver** to open the manga page in a headless browser (run in background).
2.  It is required to **answer cookie consent** and **select the reading mode** when visiting the website for the first time. It uses Selenium ActionChain to simulate user actions, such as clicking and scrolling, so that the manga pictures can be loaded into the to webpage. 
3.  There are two options when it comes to reading mode, **Vertical Follow** and **Horizontal Follow**. For my implementation, the webdriver will then find **Vertical Follow** button by its XPATH and **click** it in order to display manga pictures. However, I will try to implement the **Horizontal Follow** mode in the future because it is more efficient to download manga in this mode.
4. Most manga pictures are located in `canvas` tag of the HTML which has a URL in the `data-url` attribute linking to a **shuffled** image. They are dynamically restored and loaded by JavaScript when user the image is in close to  user's viewport. Below is an example of a shuffled image from the [Attack on Titan](https://en.wikipedia.org/wiki/Attack_on_Titan) Manga Volume 1 cover:

    <img align="center" src="https://c-1.mreadercdn.com/_v2/0/0dcb8f9eaacfd940603bd75c7c152919c72e45517dcfb1087df215e3be94206cfdf45f64815888ea0749af4c0ae5636fabea0abab8c2e938ab3ad7367e9bfa52/52/f3/52f3b6d9ac0123042cebb6fd7839fda6/52f3b6d9ac0123042cebb6fd7839fda6_1900.jpeg?t=515363393022bbd440b0b7d9918f291a&ttl=1908547557" height=300 />


