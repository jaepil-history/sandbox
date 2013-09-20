from datetime import timedelta
from tornado import web
from tornado import gen

from dataview.core import settings
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
        dashboard_model,
        discovery_model,
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

        # category = self.get_argument('category', None)
        selected_chart = self.get_argument('selected_chart', None)
        date_range = self.get_argument('date_range', None)
        date_from = self.get_argument('date_from', None)
        date_to = self.get_argument('date_to', None)
        group = self.get_argument('group', None)

        if selected_chart is None:
            selected_chart = 'all'

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

        # date_from = str(date_from)
        # date_to = str(date_to)

        all_processed_list = settings.PROCESSED_LIST

        if selected_chart:
            processed_list = selected_chart
        else:
            processed_list = all_processed_list

        print 'processed_list: ' + str(processed_list)
        print 'all_list: ' + str(all_processed_list)

        # processed_data = processed_data_model.get_processed_data(processed_list, date_from, date_to)

        # {'title',data_array} dictionary format
        dummy_data = {
            "dau": [1, 2, 3, 4, 5],
            "installs": [6, 7, 8, 9, 10],
            "removals": [11, 12, 13, 14, 15],
            "invites": [16, 17, 18, 19, 20],
            "logins": [21, 22, 23, 24, 25],
            "retention": [26, 27, 28, 29, 30],
            "viral": [31, 32, 33, 34, 35],
            "return": [36, 37, 38, 39, 40],
            "revenue": [41, 42, 43, 44, 45],
            "items": [46, 47, 48, 49, 50]
            }

        processed_data = {}

        if selected_chart == 'all':
            processed_data = dummy_data
        else:
            processed_data[selected_chart] = dummy_data[selected_chart]

        print processed_data

        self.render('index.html',
                current_page=self.current_page,
                all_processed_list=all_processed_list,
                # processed_list=processed_list,
                processed_data=processed_data,
                selected_chart=selected_chart,
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

        # category = self.get_argument('category', None)
        selected_chart = self.get_argument('selected_chart', None)
        date_range = self.get_argument('date_range', None)
        date_from = self.get_argument('date_from', None)
        date_to = self.get_argument('date_to', None)
        group = self.get_argument('group', None)

        if selected_chart is None:
            selected_chart = 'all'

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

        # date_from = str(date_from)
        # date_to = str(date_to)

        all_processed_list = settings.PROCESSED_LIST

        if selected_chart:
            processed_list = selected_chart
        else:
            processed_list = all_processed_list

        print 'processed_list: ' + str(processed_list)
        print 'all_list: ' + str(all_processed_list)

        # processed_data = processed_data_model.get_processed_data(processed_list, date_from, date_to)

        # Convert the dates to local time for display
        # date_from = utc_unixtime_to_localtime(date_from)
        # date_to = utc_unixtime_to_localtime(date_to)

        # Get the difference between UTC and localtime - used to display
        # the ticks in the charts
        zone_difference = localtime_utc_timedelta()

        # Get the max date - utc, converted to localtime
        max_date = utc_now_to_localtime()

        self.render('basic.html',
                current_page=self.current_page,
                # all_processed_list=all_processed_list,
                # processed_list=processed_list,
                # selected_data=selected_data,
                # processed_data=processed_data,
                selected_chart=selected_chart,
                date_range=date_range,
                date_from=date_from,
                date_to=date_to,
                group=group
                # zone_difference=zone_difference,
                # max_date=max_date
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


class DashboardView(BaseView):

    def initialize(self):
        super(DashboardView, self).initialize()

    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):

        active_process_checks = settings.PROCESS_CHECKS
        active_system_checks = settings.SYSTEM_CHECKS

        # Get the first element from the settings - used for the last check date in the template
        try:
            process_check_first = active_process_checks[0]
        except IndexError:
            process_check_first = False

        try:
            system_check_first = active_system_checks[0]
        except IndexError:
            system_check_first = False

        last_system_check = dashboard_model.get_last_system_check(active_system_checks)
        last_process_check = dashboard_model.get_last_process_check(active_process_checks)

        self.render("dashboard.html",
                current_page='dashboard',
                last_check=last_system_check,
                process_check=last_process_check,
                system_check_first=system_check_first,
                process_check_first=process_check_first,
                )
        self.finish()


class DiscoveryView(BaseView):

    def initialize(self):
        super(DiscoveryView, self).initialize()
        self.current_page = 'discovery'

    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):

        checked_list = self.get_arguments('checked_list', None)
        date_from = self.get_argument('date_from', False)
        date_to = self.get_argument('date_to', False)

        if date_from:
            date_from = datestring_to_utc_datetime(date_from)
        # Default - 24 hours period
        else:
            day = timedelta(hours=24)
            date_from = self.now - day

        if date_to:
            date_to = datestring_to_utc_datetime(date_to)
        else:
            date_to = self.now

        date_from = datetime_to_unixtime(date_from)
        date_to = datetime_to_unixtime(date_to)


        all_processed_list = settings.DISCOVERY

        if len(checked_list) > 0:
            selected_data = checked_list
        else:
            selected_data = all_processed_list

        processed_data = discovery_model.get_data(selected_data, date_from, date_to)
        first_check_date = discovery_model.get_first_check_date()

        # Convert the dates to local time for display
        first_check_date = utc_unixtime_to_localtime(first_check_date)
        date_from = utc_unixtime_to_localtime(date_from)
        date_to = utc_unixtime_to_localtime(date_to)

        # Get the difference between UTC and localtime - used to display
        # the ticks in the charts
        zone_difference = localtime_utc_timedelta()

        # Get the max date - utc, converted to localtime
        max_date = utc_now_to_localtime()

        if processed_data != False:
            self.render('discovery.html',
                current_page=self.current_page,
                all_processed_list=all_processed_list,
                selected_data=selected_data,
                checked_list=checked_list,
                processed_data=processed_data,
                date_from=date_from,
                date_to=date_to,
                zone_difference=zone_difference,
                max_date=max_date
                )
            self.finish()


class ProcessedDataView(BaseView):

    def initialize(self):
        super(ProcessedDataView, self).initialize()
        self.current_page = 'processed_data'

    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):

        category = self.get_argument('category', None)
        print 'category: ' + str(category)
        selected_data = self.get_arguments('selected_data', None)
        date_from = self.get_argument('date_from', False)
        date_to = self.get_argument('date_to', False)

        if date_from:
            print 'if: ' + str(date_from)
            date_from = datestring_to_utc_datetime(date_from)
        # Default - 24 hours period
        else:
            day = timedelta(hours=24)
            date_from = self.now - day
            print 'else: ' + str(date_from)

        if date_to:
            date_to = datestring_to_utc_datetime(date_to)
        else:
            date_to = self.now

        date_from = datetime_to_unixtime(date_from)
        date_to = datetime_to_unixtime(date_to)

        if category == 'discovery':
            all_processed_list = settings.DISCOVERY
        elif category == 'emails':
            all_processed_list = settings.EMAILS
        elif category == 'events':
            all_processed_list = settings.EVENTS
        elif category == 'installs':
            all_processed_list = settings.INSTALLS
        elif category == 'invites':
            all_processed_list = settings.INVITES
        elif category == 'messages':
            all_processed_list = settings.MESSAGES
        elif category == 'monetization':
            all_processed_list = settings.MONETIZATION
        elif category == 'notifications':
            all_processed_list = settings.NOTIFICATIONS
        elif category == 'virality':
            all_processed_list = settings.VIRALITY
        elif category == 'returning_users':
            all_processed_list = settings.RETURNING_USERS
        elif category == 'stream':
            all_processed_list = settings.STREAM
        elif category == 'traffic':
            all_processed_list = settings.TRAFFIC
        elif category == 'time':
            all_processed_list = settings.TIME
        elif category == 'user_distribution':
            all_processed_list = settings.USER_DISTRIBUTION
        elif category == 'user_retention':
            all_processed_list = settings.USER_RETENTION
        elif category == 'user_sessions':
            all_processed_list = settings.USER_SESSIONS
        elif category == 'unique_visitors':
            all_processed_list = settings.UNIQUE_VISITORS
        else:
            all_processed_list = settings.DISCOVERY

        print 'selected_data: ' + str(selected_data)
        print 'all_processed_list: ' + str(all_processed_list)

        if len(selected_data) > 0:
            processed_list = selected_data
        else:
            processed_list = all_processed_list

        print 'processed_list: ' + str(processed_list)

        processed_data = processed_data_model.get_processed_data(processed_list, date_from, date_to)

        # Convert the dates to local time for display
        date_from = utc_unixtime_to_localtime(date_from)
        date_to = utc_unixtime_to_localtime(date_to)

        # Get the difference between UTC and localtime - used to display
        # the ticks in the charts
        zone_difference = localtime_utc_timedelta()

        # Get the max date - utc, converted to localtime
        max_date = utc_now_to_localtime()

        self.render('processed_data.html',
                current_page=self.current_page,
                all_processed_list=all_processed_list,
                processed_list=processed_list,
                selected_data=selected_data,
                processed_data=processed_data,
                date_from=date_from,
                date_to=date_to,
                zone_difference=zone_difference,
                max_date=max_date
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
