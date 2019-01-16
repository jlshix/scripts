"""
"""

import os
import sys
import logging
from textwrap import dedent
from getopt import getopt
from datetime import datetime

import requests


def usage():
    '''print the usage of this script'''
    usage = '''
    generate hexo article
    you should exec this script at //source/_posts or its subdirectory

    Usage:
    python3 postmd.py -t TAGS -c CATEGORIES [-d DATETIME] file_path
    e.g. python3 postmd.py -t t1,t2,t3 -c c1,c2 ../dmzj/README.md
    
    filepath    md file from local directory or github
        if at github, url should starts with `https://raw.githubusercontent.com`
    -t          add `tags` attribute to file header, separated by comma
    -c          add `categories` attribute to file header, separated by comma
    -d          specify `date` attribute in format like '2019-01-16,16:41:42'
    '''
    print(usage)


def make_header(title, date, tags, categories) -> str:
    '''assemble hexo article header using given params'''
    template = dedent('''\
        ---
        title: {}
        date: {}
        tags: 
        {}
        categories:
        {}
        ---
        ''')
    header = template.format(title, date,
                ''.join(['    - {}\n'.format(li) for li in tags.split(',')]),
                ''.join(['    - {}\n'.format(li) for li in categories.split(',')]))
    return header


def hexo_new(opts: list, args: list) -> str:
    '''generate hexo article by extracting params from opts and args parsed by getopt'''
    uri = args[0]

    # get file content from github or local directory
    if uri.startswith('https://raw.githubusercontent.com'):
        resp = requests.get(uri)
        text = resp.text
    elif os.path.isfile(uri):
        with open(uri) as f:
            text = f.read()
    else:
        text = 'file not found'
        logging.warning(text)
    
    # separate title and text
    l, h = text.index('# '), text.index('\n')
    title = text[l+2:h].strip()
    text = text[h:]

    # get params
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for opt, value in opts:
        if opt == '-t':
            tags = value
        elif opt == '-c':
            categories = value
        elif opt == '-d':
            date = value.replace(',', ' ')
    
    # generate header
    header = make_header(title, date, tags, categories)

    # save file
    with open(title.replace(' ', '-')+'.md', 'w') as f:
        f.write(header)
        f.write(text)


def main():
    logging.basicConfig(level=logging.DEBUG, format=' %(levelname)s: %(message)s')

    # check argv
    if len(sys.argv) < 6:
        logging.error('args not enough')
        usage()
        exit(-1)
    # get argv
    opts, args = getopt(sys.argv[1:], 't:c:d:')
    
    # generate article
    hexo_new(opts, args)
    

if __name__ == '__main__':
    main()
