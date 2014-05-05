#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import settings


class Controller(object):

    def __init__(self, message):
        self.twitter_api = twitter.Api(
            consumer_key=settings.twitter.API_KEY,
            consumer_secret=settings.twitter.API_SECRET,
            access_token_key=settings.twitter.ACCESS_TOKEN_KEY,
            access_token_secret=settings.twitter.ACCESS_TOKEN_SECRET)
        self.message = message

    def send(self):
        self.twitter_api.PostUpdates(self.message)


def main(argv):
    if not argv:
        raise StandardError("No message")

    message = argv[0]
    c = Controller(message)
    c.send()
    print message


if __name__ == '__main__':
    raise StandardError
