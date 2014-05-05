#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class Weather(object):

    def __init__(self, location_id):
        self.location_id = location_id
        self.update()

    def update(self):
        self.data = requests.get(
            'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'
                 % self.location_id).json()

    def get_data(self):
        return self.data
