#!/usr/bin/python
# usage:
# python scraper.py <http://www.google.com>

import smtplib
import requests
import sys


_EMAIL_CONTENTS = '''
    There's been an update to the site!!
    '''


class DotDict(dict):
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def getCredentials():
    credentials = DotDict({'email': None, 'password': None})
    with open('/Users/pheven/Repositories/webscraper/credentialsfile') as f:
        credentials['email'] = f.readline().strip()
        credentials['password'] = f.readline().strip()
    return credentials


def sendEmail():
    credentials = getCredentials()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(credentials.email,
                 credentials.password)
    server.sendmail(credentials.email,
                    credentials.email,
                    _EMAIL_CONTENTS)
    server.quit()


def scrapePage(url):
    page = requests.get(url)
    new_hash = str(hash(page.text))
    with open('/Users/pheven/Repositories/webscraper/currenthash', 'r+') as f:
        h = f.read().strip()
        if h != new_hash:  # site updated!
            f.seek(0)
            f.write(str(new_hash))
            f.truncate()
            sendEmail()


def main(argv):
    url = argv[0]
    scrapePage(url)


if __name__ == '__main__':
    main(sys.argv[1:])
