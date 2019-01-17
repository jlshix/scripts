import os
import sys
import logging
import shlex
import subprocess
from textwrap import dedent
import argparse
from datetime import datetime

import requests

domain = 'http://leoshi.me'
server = 'http://jlshix.com:4000'

def shell(command: str) -> str:
    """exec shell command and return output string"""
    logging.info('running `{}`...'.format(command))
    return subprocess.check_output(shlex.split(command)).decode().strip('\n')


def deploy(clean=False, preview=False):
    '''deploy to github pages'''
    if clean:
        shell('hexo clean')
    shell('hexo g')
    if preview:
        shell('hexo s')
        logging.info('start server at {}, ctrl+c to stop server'.format(server))
        choice = input('would you like to deploy on {} ? (yes/no, default yes)'.format(domain))
        if choice.startswith('n'):
            logging.info('exit because you choosed no')
            return
        elif choice != '\n' or not choice.startswith('y'):
            logging.info('exit because of unknown choice')
            return
    logging.info('start deploying...')
    shell('hexo d')
    logging.info('deployed')

    
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


def hexo_new(args):
    '''generate hexo article by extracting params from args'''
    uri = args.uri

    logging.info('featching file...')
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

    logging.info('generating header...')
    # get params
    tags, categories, date, name = args.t, args.c, args.d, args.n
    if not date:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not name:
        name = title.replace(' ', '-')+'.md'
    if not name.endswith('.md'):
        name += '.md'
    # generate header
    header = make_header(title, date, tags, categories)

    # save file
    logging.info('saving file {}...'.format(name))
    with open(name, 'w') as f:
        f.write(header)
        f.write(text)
    logging.info('done generating new file')


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    # root parser with description, all text below are aranged into `--help`
    parser = argparse.ArgumentParser(description='generate new hexo file and deply for hexo, you should exec this script at //source/_posts or its subdirectory')
    # specify subcommand
    subparsers = parser.add_subparsers(dest='cmd')

    # subcommand `deploy` with option `-clean`, TODO `-preview`
    deployer = subparsers.add_parser('deploy', description='deploy to github pages')
    deployer.add_argument('-c', '-clean', action='store_true', help='clean before generate')

    # subcommand `new`
    gene = subparsers.add_parser('new', description='new hexo article from local or github')
    gene.add_argument('uri', help=('md file from local directory or github'
            'if at github, url should starts with `https://raw.githubusercontent.com`'))
    gene.add_argument('-t', '-tag', help='add `tags` attribute to file header, separated by comma')
    gene.add_argument('-c', '-cat', help='add `categories` attribute to file header, separated by comma')
    gene.add_argument('-d', '-date', help='specify `date` attribute in format like `2019-01-16,16:41:42`')
    gene.add_argument('-n', '-name', help='default name is title in content, specify to rename it')

    args = parser.parse_args()
    logging.info(args)

    if not args.cmd:
        logging.error('no command specified')
        exit(-1)
    elif args.cmd == 'deploy':
        deploy(clean=args.c)
    elif args.cmd == 'new':
        hexo_new(args) 
    # else option is not necessary

if __name__ == "__main__":
    main()