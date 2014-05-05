#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
import hashlib
import twitter
import settings
import datetime


def get_letters():  
    source = string.digits + string.letters
    letters = u"".join([random.choice(source) for i in xrange(25)])
    letters_hash = hashlib.sha256(letters).hexdigest()
    return letters_hash


def tweet(message):
    twitter_api = twitter.Api(
        consumer_key=settings.twitter.API_KEY,
        consumer_secret=settings.twitter.API_SECRET,
        access_token_key=settings.twitter.ACCESS_TOKEN_KEY,
        access_token_secret=settings.twitter.ACCESS_TOKEN_SECRET)
    twitter_api.PostUpdates(message)


def main(argv):
    message = u" ".join([
        u"[自動テスト]", 
        u"【date】:",
        unicode(datetime.datetime.now()),
        u"【code】:",
        get_letters(),
    ])
    tweet(message)
    print message


if __name__ == '__main__':
    raise StandardError

