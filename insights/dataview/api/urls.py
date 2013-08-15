from dataview.api import handlers

'''
http://query.kontagent.net/processed/v1/users/gender_distribution/<data_type>.<data_format>/?api_key=<API KEY>&<other parameters>
http://query.kontagent.net/processed/v1/users/age_distribution/<data_type>.<data_format>/?api_key=<API KEY>&<other parameters>
http://query.kontagent.net/processed/v1/users/friends_distribution/<data_type>.<data_format>/?api_key=<API KEY>&<other parameters>
http://query.kontagent.net/processed/v1/users/country_distribution/<data_type>.<data_format>/?api_key=<API KEY>&<other parameters>

http://query.kontagent.net/processed/v1/messages/discovery_clicks/series.json/?start_time=20110605_0000&api_key=&time_segment=week&end_time=20110705_0000&discovery_type=nf
http://query.kontagent.net/processed/v1/events/count/dict.json/?start_time=20121007_0000&api_key=&time_segment=day&end_time=20121107_0000
http://query.kontagent.net/processed/v1/events/distribution/dict.json/?api_key=<API KEY>&<other parameters>
http://query.kontagent.net/processed/v1/events/names/list.json/?api_key=<API_KEY>
etc...
'''

handlers = [
    (r"/processed/v1/messages/discovery_clicks/", handlers.DiscoveryHandler),

    (r"/processed/v1/messages/email_conversion/", handlers.EmailConversionHandler),
    (r"/processed/v1/messages/email_events/", handlers.EmailEventsHandler),
    (r"/processed/v1/messages/email_limit/", handlers.EmailLimitHandler),
    (r"/processed/v1/messages/emails_received/", handlers.EmailsReceivedHandler),
    (r"/processed/v1/messages/emails_responses/", handlers.EmailsResponsesHandler),
    (r"/processed/v1/messages/emails_sent/", handlers.EmailsSentHandler),

    (r"/processed/v1/messages/invite_conversion/", handlers.InviteConversionHandler),
    (r"/processed/v1/messages/invite_events/", handlers.InviteEventsHandler),
    (r"/processed/v1/messages/invite_limit/", handlers.InviteLimitHandler),
    (r"/processed/v1/messages/invites_received/", handlers.InvitesReceivedHandler),
    (r"/processed/v1/messages/invite_responses/", handlers.InviteResponsesHandler),
    (r"/processed/v1/messages/invites_sent/", handlers.InvitesSentHandler),

    (r"/processed/v1/messages/messages_sent/", handlers.MessagesSentHandler),
    (r"/processed/v1/messages/messages_clicks/", handlers.MessagesClicksHandler),
    (r"/processed/v1/messages/messages_responses/", handlers.MessagesResponsesHandler),

    (r"/processed/v1/messages/notification_conversion/", handlers.NotificationConversionHandler),
    (r"/processed/v1/messages/notification_events/", handlers.NotificationEventsHandler),
    (r"/processed/v1/messages/notification_limit/", handlers.NotificationLimitHandler),
    (r"/processed/v1/messages/notifications_sent/", handlers.NotificationsSentHandler),
    (r"/processed/v1/messages/notifications_received/", handlers.NotificationsReceivedHandler),
    (r"/processed/v1/messages/notifications_responses/", handlers.NotificationsResponsesHandler),

    (r"/processed/v1/messages/stream_posts/", handlers.StreamPostHandler),
    (r"/processed/v1/messages/stream_responses/", handlers.StreamResponseHandler),
    (r"/processed/v1/messages/stream_clicks/", handlers.ExternalLinkClickHandler),
    (r"/processed/v1/messages/stream_post_click_ratio/", handlers.StreamPostClickRatioHandler),

    (r"/processed/v1/monetization/revenue/", handlers.MonetizationRevenueHandler),
    (r"/processed/v1/monetization/transactions/", handlers.MonetizationTransactionsHandler),
    (r"/processed/v1/monetization/average_transaction/", handlers.MonetizationAverageTransactionHandler),
    (r"/processed/v1/monetization/arppu/", handlers.MonetizationARPPUHandler),
    (r"/processed/v1/monetization/spending_users/", handlers.MonetizationSpendingUsersHandler),

    (r"/processed/v1/traffic_sources/clicks/", handlers.TrafficClicksHandler),
    (r"/processed/v1/traffic_sources/install_summary/", handlers.TrafficInstallSummaryHandler),
    (r"/processed/v1/traffic_sources/installs/", handlers.TrafficInstallsHandler),
    (r"/processed/v1/traffic_sources/summary/", handlers.TrafficSummaryHandler),

    (r"/processed/v1/events/count/", handlers.EventsCountHandler),
    (r"/processed/v1/events/distribution/", handlers.EventsDistributionHandler),
    (r"/processed/v1/events/names/", handlers.EventsNamesHandler),
    (r"/processed/v1/events/names_subtree/", handlers.EventsNamesSubtreeHandler),
    (r"/processed/v1/events/value/", handlers.EventsValueHandler),
    (r"/processed/v1/events/goal_counts/", handlers.GoalCountsHandler),
    (r"/processed/v1/events/pageviews/", handlers.PageViewsHandler),

    (r"/processed/v1/users/gender_distribution/", handlers.UsersGenderDistributionHandler),
    (r"/processed/v1/users/age_distribution/", handlers.UsersAgeDistributionHandler),
    (r"/processed/v1/users/friends_distribution/", handlers.UsersFriendsDistributionHandler),
    (r"/processed/v1/users/country_distribution/", handlers.UsersCountryDistributionHandler),
    (r"/processed/v1/users/virality/", handlers.UsersViralityHandler),
    (r"/processed/v1/users/returning/", handlers.UsersReturningUsersHandler),
    (r"/processed/v1/users/uniques/", handlers.UsersUniqueVisitorsHandler),
    (r"/processed/v1/users/uniques_rolling/", handlers.UsersUniqueRollingHandler),
    (r"/processed/v1/users/retention/", handlers.UsersRetentionHandler),
    (r"/processed/v1/users/installs_all/", handlers.InstallsAllHandler),
    (r"/processed/v1/users/installs_unique/", handlers.InstallsUniqueHandler),
    (r"/processed/v1/users/removes/", handlers.RemovesHandler),

    (r"/processed/v1/session/count/", handlers.UserSessionsHandler),
    (r"/processed/v1/session/avg_length/", handlers.UserSessionsHandler)
]
