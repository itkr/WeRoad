#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import settings

twitter_api = twitter.Api(
    consumer_key=settings.twitter.API_KEY,
    consumer_secret=settings.twitter.API_SECRET,
    access_token_key=settings.twitter.ACCESS_TOKEN_KEY,
    access_token_secret=settings.twitter.ACCESS_TOKEN_SECRET)
