#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import settings
import datetime
from models import Weather


class Controller(object):

    def __init__(self, location_id):
        self.twitter_api = twitter.Api(
            consumer_key=settings.twitter.API_KEY,
            consumer_secret=settings.twitter.API_SECRET,
            access_token_key=settings.twitter.ACCESS_TOKEN_KEY,
            access_token_secret=settings.twitter.ACCESS_TOKEN_SECRET)

        # TODO: dataを隠蔽
        self.wheather = Weather(location_id).get_data()

    def get_weekday_name(self, date):
        return [u"月", u"火", u"水", u"木", u"金", u"土", u"日"][date.weekday()]

    def get_weekday_message(self, date):
        message = [
            u"今週もぼんぼりましょう_(´ཀ`」 ∠)_",
            u"深夜アニメまで頑張ろう_(:3 ⌒ﾞ)_",
            u"働きたくないでござる(´；ω；｀)",
            u"中途半端な曜日やね！",
            u"もうすぐ週末＼＼\\ ٩( 'ω' )و //／／",
            u"今日は何しようか(´⊙ω⊙｀)",
            u"｜ω・）月曜日の影", ]
        return message[date.weekday()]

    # TODO: ストラテジパターンとか使って分ける
    def make_message(self):
        prefecture = self.wheather.get("location").get("prefecture")  # 都道府県
        for forecasts in self.wheather.get("forecasts"):
            if forecasts.get("dateLabel") == u"今日":
                break
        today = datetime.datetime.strptime(forecasts.get("date"), '%Y-%m-%d')
        weekday = self.get_weekday_name(today)
        public_time = self.wheather.get("publicTime")

        max_temperature = min_temperature = None
        if forecasts.get("temperature").get("max"):
            max_temperature = forecasts.get("temperature").get("max").get('celsius')
        if forecasts.get("temperature").get("min"):
            min_temperature = forecasts.get("temperature").get("min").get('celsius')

        if max_temperature and min_temperature:
            message_format = u"[自動] おはよう。 {month}月{day}日({weekday}) {prefecture}は{telop} 気温{min_temperature}〜{max_temperature}度 {extend_message}"
        elif max_temperature:
            message_format = u"[自動] おはよう。 {month}月{day}日({weekday}) {prefecture}は{telop} 最高気温は{max_temperature}度です {extend_message}"
        elif min_temperature:
            message_format = u"[自動] おはよう。 {month}月{day}日({weekday}) {prefecture}は{telop} 最低気温は{min_temperature}度です {extend_message}"
        else:
            message_format = u"[自動] おはよう。 {month}月{day}日({weekday}) {prefecture}の天気は{telop}みたいです。 {extend_message}"

        return message_format.format(
            month=today.month,
            day=today.day,
            weekday=weekday,
            prefecture=prefecture,
            telop=forecasts.get("telop"),  # "晴れ"など
            max_temperature=max_temperature,  # 最高気温
            min_temperature=min_temperature,  # 最低気温
            extend_message=self.get_weekday_message(today))

    def send(self):
        message = self.make_message()
#        self.twitter_api.PostUpdates(message)
        return message


def main(argv):
    location_id = argv[0] if argv else 130010
    print "location_id:", location_id
    c = Controller(location_id)
    message = c.send()
    print "".join([message, u" 【", str(len(message)), u"文字】"])


if __name__ == '__main__':
    raise StandardError
