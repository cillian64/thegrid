#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Dr House Industries'
SITENAME = 'The·Grid'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['images', 'extra']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/bodges.css': {'path': 'bodges.css'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/proposal.pdf': {'path': 'proposal.pdf'},
    'extra/quotes.js': {'path': 'quotes.js'},
    'extra/redirects/1': {'path': 'welcome.html'},
    'extra/redirects/2': {'path': 'approval.html'},
    'extra/redirects/3': {'path': '175m-aluminium-angle-on-its-way.html'},
    'extra/redirects/4': {'path': 'another-day-another-order.html'},
    'extra/redirects/5': {'path': 'psus-arrived-aluminium-didnt.html'},
    'extra/redirects/6': {'path': 'aluminium-arrived-at-last.html'},
    'extra/redirects/7': {'path': 'rework-and-a-pcb.html'},
    'extra/redirects/8': {'path': 'testing-led-strips-and-a-psu.html'},
    'extra/redirects/9': {'path': 'control-software.html'},
}

YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'
DAY_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/index.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'Blog'
ARTICLE_EXCLUDES = ['pages']

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pin_to_top']

TIMEZONE = 'Europe/London'
DEFAULT_LANG = 'en'

# Make quotes look pretty
TYPOGRIFY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DISPLAY_PAGES_ON_MENU = True
DEFAULT_PAGINATION = False
SUMMARY_MAX_LENGTH = 300

THEME = "themes/pelican-bootstrap3"
BOOTSTRAP_THEME = "cyborg"
SHOW_ARTICLE_AUTHOR = True


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

LINKS = (('EMF 2014', 'http://emfcamp.org'),)
SOCIAL = (('Twitter', 'https://twitter.com/__thegrid'),)
