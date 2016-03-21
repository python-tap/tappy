# Copyright (c) 2016, Matt Layman

from ConfigParser import ConfigParser, NoOptionError, NoSectionError
import os
import sys

import requests

API_URL = 'https://www.transifex.com/api/2'
LANGUAGES = [
    'ar',
    'de',
    'es',
    'fr',
    'it',
    'ja',
    'nl',
    'pt',
    'ru',
    'zh',
]


def fetch_po_for(language, username, password):
    print 'Downloading po file for {0} ...'.format(language)
    po_api = '/project/tappy/resource/tappypot/translation/{0}/'.format(
        language)
    po_url = API_URL + po_api
    params = {'file': '1'}
    r = requests.get(po_url, auth=(username, password), params=params)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        output_file = os.path.join(
            here, 'tap', 'locale', language, 'LC_MESSAGES', 'tappy.po')
        with open(output_file, 'wb') as out:
            out.write(r.text.encode('utf-8'))
    else:
        print('Something went wrong fetching the {0} po file.'.format(
            language))


def get_auth_from_conf(here):
    transifex_conf = os.path.join(here, '.transifex.ini')
    config = ConfigParser()
    try:
        with open(transifex_conf, 'r') as conf:
            config.readfp(conf)
    except IOError as ex:
        sys.exit('Failed to load authentication configuration file.\n'
                 '{0}'.format(ex))
    try:
        username = config.get('auth', 'username')
        password = config.get('auth', 'password')
    except (NoOptionError, NoSectionError) as ex:
        sys.exit('Oops. Incomplete configuration file: {0}'.format(ex))

    return username, password

if __name__ == '__main__':
    here = os.path.abspath(os.path.dirname(__file__))
    username, password = get_auth_from_conf(here)

    for language in LANGUAGES:
        fetch_po_for(language, username, password)
