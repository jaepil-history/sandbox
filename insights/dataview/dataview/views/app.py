#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from tornado import web
from tornado import gen

from dataview.config import settings
from dataview.views.base import BaseView
from dataview.utils.dates import (
        datestring_to_utc_datetime,
        datestring_to_utc_date,
        datetime_to_unixtime,
        utc_unixtime_to_localtime,
        localtime_utc_timedelta,
        utc_now_to_localtime
        )
from dataview.views.models import (
        processed_data_model,
        user_model
        )


class MainView(BaseView):

    def initialize(self):
        super(MainView, self).initialize()

    @web.authenticated
    def get(self):
        self.redirect('/index')


class IndexView(BaseView):

    def initialize(self):
        super(IndexView, self).initialize()
        self.current_page = 'index'

    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):

        app_id = self.get_argument('app_id', None)
        selected_chart = self.get_argument('selected_chart', None)
        date_range = self.get_argument('date_range', None)
        date_from = self.get_argument('date_from', None)
        date_to = self.get_argument('date_to', None)
        group = self.get_argument('group', None)

        print 'request: ' + self.request.uri

        # default : meteos app_id
        if app_id is None:
            #app_id = "5226e77335b6e61184d73e39"
            app_id = settings.APP_ID

        if date_range is None:
            date_range = '30' # default 30 days

        if group is None:
            group = 'None'

        if date_range != 'custom':
            period = int(date_range)
            date_from = self.now - timedelta(days=period)
            date_to = self.now - timedelta(days=1)
        elif date_range == 'custom':
            date_from = datestring_to_utc_date(date_from)
            date_to = datestring_to_utc_date(date_to)
            if (date_to - date_from).days < 0:
                temp = date_from
                date_from = date_to
                date_to = temp
        else:
            print 'date_range is not proper'

        all_charts = settings.PROCESSED_LIST
        charts_list = []

        if selected_chart is None or selected_chart == 'All':
            charts_list = all_charts
        else:
            charts_list.append(selected_chart)

        print 'all_list: ' + str(all_charts)
        print 'selected: ' + str(charts_list)

        charts_data = processed_data_model.get_processed_data(app_id, charts_list, date_from, date_to)

        for key in charts_list:
            temp_list = []
            if key == 'Retention':
                for i in range(len(charts_data[key])):
                    temp = {}
                    doc = charts_data[key][i]
                    temp['date'] = doc['t'].encode('ascii', 'ignore')
                    temp['ret'] = doc['ret']

                    temp_list.append(temp)

                charts_data[key] = temp_list

            elif key == 'PU':
                usd_pu = []
                kwn_pu = []
                for i in range(len(charts_data[key])):
                    doc = charts_data[key][i]

                    for item in temp_list:
                        if item['date'] == doc['t'].encode('ascii', 'ignore'):
                            item[doc['currency'].encode('ascii', 'ignore')] = doc['counts']
                            break

                    else:
                        temp = {}
                        temp['date'] = doc['t'].encode('ascii', 'ignore')
                        temp[doc['currency'].encode('ascii', 'ignore')] = doc['counts']
                        temp_list.append(temp)

                charts_data[key] = temp_list
                print 'revenue data: ' + str(charts_data[key])

            elif key == 'Revenue':
                # Revenue_USD & Revenue_KWN : {'date': '2013-09-13', 'usd': 20031L, 'kwn': 78900L}
                for i in range(len(charts_data[key])):
                    doc = charts_data[key][i]

                    for item in temp_list:
                        if item['date'] == doc['t'].encode('ascii', 'ignore'):
                            item[doc['currency'].encode('ascii', 'ignore')] = int(doc['revenue'])
                            break

                    else:
                        temp = {}
                        temp['date'] = doc['t'].encode('ascii', 'ignore')
                        temp[doc['currency'].encode('ascii', 'ignore')] = int(doc['revenue'])
                        temp_list.append(temp)

                charts_data[key] = temp_list
                #print 'revenue data: ' + str(charts_data[key])

            else:
                for i in range(len(charts_data[key])):
                    temp = {}
                    doc = charts_data[key][i]
                    temp['date'] = doc['t'].encode('ascii', 'ignore')
                    temp['counts'] = doc['counts']

                    if group == 'level':
                        if key != 'Installs':
                            temp['level'] = doc['lv']
                    elif group == 'friends':
                        temp['friends'] = doc['f']
                    else:
                        pass

                    temp_list.append(temp)

                charts_data[key] = temp_list


        self.render('index.html',
                current_page=self.current_page,
                all_charts=all_charts,
                charts_list=charts_list,
                selected_chart=selected_chart,
                charts_data=charts_data,
                date_range=date_range,
                date_from=date_from,
                date_to=date_to,
                group=group
        )
        self.finish()


class BasicView(BaseView):

    def initialize(self):
        super(BasicView, self).initialize()
        self.current_page = 'basic'

    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):

        selected_chart = self.get_argument('selected_chart', None)
        date_range = self.get_argument('date_range', None)
        date_from = self.get_argument('date_from', None)
        date_to = self.get_argument('date_to', None)
        group = self.get_argument('group', None)

        print 'request: ' + self.request.uri

        if date_range is None:
            date_range = '1'

        if group is None:
            group = 'None'

        if date_range != 'custom':
            period = int(date_range)
            date_from = self.now - timedelta(days=period)
            date_to = self.now - timedelta(days=1)
        elif date_range == 'custom':
            date_from = datestring_to_utc_date(date_from)
            date_to = datestring_to_utc_date(date_to)
            if (date_to - date_from).days < 0:
                temp = date_from
                date_from = date_to
                date_to = temp
        else:
            print 'date_range is not proper'

        all_charts = settings.PROCESSED_LIST
        charts_list = []

        if selected_chart is not None:
            charts_list.append(selected_chart)
        else:
            charts_list = all_charts

        print 'charts_list: ' + str(charts_list)
        print 'all_list: ' + str(all_charts)

        # charts_data = processed_data_model.get_processed_data(charts_list, date_from, date_to)

        # {'title',data_array} dictionary format
        dummy_data = {
            "DAU": [1, 2, 3, 4, 5],
            "Installs": [6, 7, 8, 9, 10],
            "Removals": [11, 12, 13, 14, 15],
            "Invites": [16, 17, 18, 19, 20],
            "Logins": [21, 22, 23, 24, 25],
            "Retention": [26, 27, 28, 29, 30],
            "Virality": [31, 32, 33, 34, 35],
            "Returning": [36, 37, 38, 39, 40],
            "Revenue": [41, 42, 43, 44, 45],
            "Items": [46, 47, 48, 49, 50]
            }

        charts_data = {}

        for title in charts_list:
            charts_data[title] = dummy_data[title]

        print 'charts_data: ' + str(charts_data)

        self.render('basic.html',
                current_page=self.current_page,
                all_charts=all_charts,
                charts_list=charts_list,
                selected_chart=selected_chart,
                charts_data=charts_data,
                date_range=date_range,
                date_from=date_from,
                date_to=date_to,
                group=group
        )
        self.finish()


class AnalyticsView(BaseView):

    def initialize(self):
        super(AnalyticsView, self).initialize()

    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):

        self.render("analytics.html",
                current_page='analytics',
                )
        self.finish()


class OperationView(BaseView):

    def initialize(self):
        super(OperationView, self).initialize()

    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):

        self.render("operation.html",
                current_page='operation',
                )
        self.finish()


class SettingsView(BaseView):

    def initialize(self):
        super(SettingsView, self).initialize()
        self.current_page = 'settings'

    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):

        # Get the max date - utc, converted to localtime
        max_date = utc_now_to_localtime()

        self.render('settings.html',
            max_date=max_date,
            current_page=self.current_page
        )
        self.finish()


class SettingsChangePasswordView(BaseView):

    def initialize(self):
        super(SettingsChangePasswordView, self).initialize()
        self.current_page = 'settings'

    @web.authenticated
    def post(self):

        new_password = self.get_argument('new-password')
        user_model.update_password(self.current_user, new_password)

        self.redirect('/settings')
