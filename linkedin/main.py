import sys
import json

from .linkedin import write_jobs, word_count, JOBS

def main():
    len_argv = len(sys.argv)
    if len_argv < 2:
            pass
    elif len_argv==2 and sys.argv[1] == '--write_jobs':
        write_jobs()
    else:
        print('Wrong usage. Use --write_jobs to write text for jobs in URLS (urls.py) and count or run '
            'without arguments to read previously saved jobs text and count.')
        sys.exit()
        
    with open(JOBS, 'r') as f:
        text = json.load(f)
    word_counter = word_count(text)
    print('Keyword: Number of jobs the keyword appeared')
    for keyword, count in word_counter:
        print(f'{keyword}: {count}')