#!/usr/bin/python

import smtplib
from lxml import html
import requests


"""Silly script to send email updates from a web scrape.

Crontab config:
    05 8 * * * pheven /blogScraper.py "Runs at 08:05 every day"

Requires lxml and requests modules:
    $ sudo pip install requests
    $ sudo pip install lxml

Update the path if things are hosed:
    $ export \
    PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}"
"""

_URL = 'http://planetpython.org/'
_HR = '//*[@id="body-main"]/hr[1]'


class DotDict(dict):
    """Unnecessary dict subclass.

    Lets you access dictionary members via dot notation.
    https://docs.python.org/2/reference/datamodel.html
    """

    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def scrapePage():
    """Scrape and html page.

    http://docs.python-guide.org/en/latest/scenarios/scrape/
    """

    page = requests.get(_URL)
    tree = html.fromstring(page.content)
    # start of post
    post_start = tree.xpath(_HR)[0]
    post_contents = ['From: ' + _URL]
    for i in post_start.itersiblings():
        if i.tag == 'h2':  # end of post
            break
        else:
            post_contents.append(i.text_content())

    return '\n'.join(post_contents)


def getCredentials():
    credentials = DotDict({'email': None, 'password': None})
    with open('credentialsFile') as f:
        credentials['email'] = f.readline().strip()
        credentials['password'] = f.readline().strip()
    return credentials


def sendEmail(email_contents=None):
    credentials = getCredentials()

    if email_contents:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(credentials.email,
                     credentials.password)
        server.sendmail(credentials.email,
                        credentials.email,
                        email_contents)
        server.quit()


def main():
    email_contents = scrapePage()
    try:
        sendEmail(email_contents)
    except Exception, e:
        raise e


if __name__ == '__main__':
    main()
