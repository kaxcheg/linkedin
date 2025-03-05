import requests
import json
import os
import time
import re
from collections import Counter
from bs4 import BeautifulSoup

script_dir = os.path.dirname(os.path.abspath(__file__))

URLS = os.path.join(script_dir,'urls.json')
JOBS = os.path.join(script_dir, 'jobs.json')
KEYWORDS = os.path.join(script_dir, 'keywords.json')

def write_jobs():
    """Writes JOBS file with scraped text of lists and listed paragraphs from pages listed in urls.py"""
    with open(URLS, 'r') as f:
        urls = json.load(f)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    if os.path.exists(JOBS):
        with open(JOBS, 'w'):
            pass

    with requests.Session() as session:
        session.headers.update(headers)
        jobs = []
        for url in urls:
                response = session.get(url=url, headers=headers)
                try:
                    response.raise_for_status()
                except:
                    jobs.append(f'URL skipped for HTTP error response: {response.reason}')
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')
                about = soup.find('section', class_='show-more-less-html')
                if about:
                    job = ''
                    paragraphs = about.find_all(['p'])
                    for paragraph in paragraphs:
                        par_text = paragraph.get_text(strip=True)
                        if par_text.startswith('•'):
                            job += par_text.replace('•', '') + '\n'
                                                          
                    list_elements = about.find_all(['li'])
                    job += '\n'.join(element.get_text(strip=True) for element in list_elements)
                    jobs.append(job)
                    
                time.sleep(1.0)

        with open(JOBS, 'w') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=4)

def word_count(jobs_list:list[str]) -> list:
    """Returns sorted list of Counters keywords from KEYWORDS file with counters of how many 
    times this word (if keyword is a word) or any of words from the list (if keyword is a list) has been found in JOBS file."""

    with open(KEYWORDS, 'r') as f:
        keywords = json.load(f)

    word_counter = Counter()
    for job_text in jobs_list:
        keywords_found_in_job = set()
        job_text_lower = job_text.lower()
        for keyword in keywords:
            if isinstance(keyword, list):
                for entry in keyword:
                    pattern = r'(?<!\w)' + re.escape(entry.lower()) + r'(?!\w)'
                    if re.search(pattern, job_text_lower):
                        keywords_found_in_job.add(' OR '.join(keyword))
                        break
            else:
                pattern = r'(?<!\w)' + re.escape(keyword.lower()) + r'(?!\w)'
                if re.search(pattern, job_text_lower):
                    keywords_found_in_job.add(keyword)
        word_counter.update(keywords_found_in_job)
    
    sorted_word_counter = sorted(word_counter.items(), key=lambda item: item[1], reverse=True)

    return sorted_word_counter