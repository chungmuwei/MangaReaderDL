from setuptools import setup, find_packages

# Read the dependencies from requirements.txt

with open('requirements.txt') as f:
    dependencies = f.read().splitlines()

with open('readme.md') as f:
    long_description = f.read()

setup(
    name='manga-dl',
    version='0.3.0',
    description='Download manga from mangareader.to website by the URL of the manga chapter/volume',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mu-Wei Chung',
    author_email='raymondc0302@gmail.com',
    url='https://github.com/chungmuwei/MangaReaderDL',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'manga-dl=app.manga_dl:main',
        ],
    },
    install_requires= dependencies,
    classifiers=[
        'Development Status :: 4 - Beta',  
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',  
        'Programming Language :: Python :: 3.11.1',  
    ],
)
