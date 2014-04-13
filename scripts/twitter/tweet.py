#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import settings
import requests
import datetime


class Weather(object):

    def __init__(self, location_id):
        self.data = requests.get(
            'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' \
                 % location_id).json()

    def get_data(self):
        return self.data


class Contoroller(object):
    LOCATION_ID = 130010

    def __init__(self):
        self.twitter_api = twitter.Api(
            consumer_key=settings.twitter.API_KEY,
            consumer_secret=settings.twitter.API_SECRET,
            access_token_key=settings.twitter.ACCESS_TOKEN_KEY,
            access_token_secret=settings.twitter.ACCESS_TOKEN_SECRET)

        # TODO: dataを隠蔽
	self.wheather = Weather(self.LOCATION_ID).get_data()

    # TODO: ストラテジパターンとか使って分ける
    def make_message(self):
        prefecture = self.wheather.get("location").get("prefecture")  # 都道府県
	for forecasts in self.wheather.get("forecasts"):
            if forecasts.get("dateLabel") == u"今日":
                break
	max_temperature = forecasts.get("temperature").get('max').get('celsius')  # 最高気温
        min_temperature = forecasts.get("temperature").get('min').get('celsius')  # 最高気温
        today = datetime.datetime.strptime(forecasts.get("date"), '%Y-%m-%d')  # 日付
        month = today.month
        day = today.day
	telop = forecasts.get("telop")  # "晴れ"など
	public_time = self.wheather.get("publicTime")
        message = u"[自動送信テスト] {month}月{day}日 {prefecture}の天気は{telop}、最高気温{max_temperature}度 最低気温{min_temperature}度".format(month=month, day=day, prefecture=prefecture, telop=telop, max_temperature=max_temperature, min_temperature=min_temperature)
        return message

    def send(self):
        print self.make_message()
        self.twitter_api.PostUpdates(self.make_message())


c = Contoroller()
c.send()
