from datetime import timedelta
from tornado.web import authenticated
from dataview.core import settings
from dataview.views.base import BaseView
from dataview.utils.dates import (
        datestring_to_utc_datetime,
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

class DashboardView(BaseView):

    def initialize(self):
        super(DashboardView, self).initialize()

    @authenticated
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


class DiscoveryView(BaseView):

    def initialize(self):
        super(DiscoveryView, self).initialize()
        self.current_page = 'discovery'

    @authenticated
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



class ProcessedDataView(BaseView):

    def initialize(self):
        super(ProcessedDataView, self).initialize()
        self.current_page = 'processed_data'

    @authenticated
    def get(self):

        selected_data = self.get_arguments('selected_data', None)
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


        all_processed_list = settings.PROCESSED_LIST

        if len(selected_data) > 0:
            processed_list = selected_data
        else:
            processed_list = settings.PROCESSED_LIST

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


class SettingsView(BaseView):

    def initialize(self):
        super(SettingsView, self).initialize()
        self.current_page = 'settings'

    @authenticated
    def get(self):

        # Get the max date - utc, converted to localtime
        max_date = utc_now_to_localtime()

        self.render('settings.html',
            max_date=max_date,
            current_page=self.current_page,
        )


class SettingsChangePasswordView(BaseView):

    def initialize(self):
        super(SettingsChangePasswordView, self).initialize()
        self.current_page = 'settings'

    @authenticated
    def post(self):

        new_password = self.get_argument('new-password')
        user_model.update_password(self.current_user, new_password)

        self.redirect('/settings')
