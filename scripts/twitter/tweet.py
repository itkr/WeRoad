#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs

import twitter
import settings
import requests
import datetime


class Weather(object):

    def __init__(self, location_id):
        self.data = requests.get(
            'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'
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
        today = datetime.datetime.strptime(forecasts.get("date"), '%Y-%m-%d')
        public_time = self.wheather.get("publicTime")

        if forecasts.get("temperature").get("max"):
            message = u"[自動] おはよう。 {month}月{day}日 {prefecture}は{telop} 気温{min_temperature}〜{max_temperature}度"\
                .format(month=today.month,
                        day=today.day,
                        prefecture=prefecture,
                        telop=forecasts.get("telop"),  # "晴れ"など
                        max_temperature=forecasts.get("temperature").get('max').get('celsius'),  # 最高気温
                        min_temperature=forecasts.get("temperature").get('min').get('celsius'))  # 最低気温
        else:
            message = u"[自動] おはよう。 {month}月{day}日 {prefecture}の天気は{telop}みたいです。"\
                .format(month=today.month,
                        day=today.day,
                        prefecture=prefecture,
                        telop=forecasts.get("telop"))  # "晴れ"など
        return message

    def send(self):
        message = self.make_message()
        self.twitter_api.PostUpdates(message)
        print message


def main():
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    c = Contoroller()
    c.send()


if __name__ == '__main__':
    main()
