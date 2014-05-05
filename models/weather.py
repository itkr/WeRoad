#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime


class Weather(object):

    def __init__(self, location_id):
        self.data = requests.get(
            'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'
                 % location_id).json()

    def get_data(self):
        return self.data
