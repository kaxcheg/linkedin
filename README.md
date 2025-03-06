# Description
This is small keyword counter in Linkedin jobs. It prints number of jobs, where a keyword has appeared, for each keyword. Jobs are Linkedin jobs web pages. Keywords are names of skills, products etc. and could be strings or list of strings (in this case appearance of any word from the list is counts). 
Scraping is optimized searching only in lists and listing paragraphs, where keywords are presented in 90% vacancies.

# Requirements
- requests
- beautifulsoup4

# Install
```
pip install git+https://github.com/kaxcheg/linkedin.git
```
# Usage
Put job pages urls in urls.json and keywords in keywords.json. See keywords.json and urls.json for my examples.

Run to write job texts to jobs.json and count keywords (uses requests, more slow):
```
py -m linkedin --write_jobs
```
Run to count keywords in previously written file (only counts - fast):
```
py -m linkedin
```
# Testing
Clone repository:
```
git clone https://github.com/kaxcheg/linkedin.git
```
Run tests from tests folder:
```
py -m unittest discover
```