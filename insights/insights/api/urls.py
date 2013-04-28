import handlers

handlers = [
    (r"/api/v1/[0-9A-Fa-f]+/apa/", handlers.ApplicationAddedHandler),
    (r"/api/v1/[0-9A-Fa-f]+/apr/", handlers.ApplicationRemovedHandler),
    (r"/api/v1/[0-9A-Fa-f]+/cpu/", handlers.UserInformationHandler),
    (r"/api/v1/[0-9A-Fa-f]+/evt/", handlers.CustomEventHandler),
    (r"/api/v1/[0-9A-Fa-f]+/ins/", handlers.InviteSentHandler),
    (r"/api/v1/[0-9A-Fa-f]+/inr/", handlers.InviteReceivedHandler),
    (r"/api/v1/[0-9A-Fa-f]+/gci/", handlers.GoalCountsHandler),
    (r"/api/v1/[0-9A-Fa-f]+/mtu/", handlers.RevenueTrackingHandler),
    (r"/api/v1/[0-9A-Fa-f]+/pgr/", handlers.PageRequestHandler),
    (r"/api/v1/[0-9A-Fa-f]+/pst/", handlers.StreamPostHandler),
    (r"/api/v1/[0-9A-Fa-f]+/psr/", handlers.StreamResponseHandler),
    (r"/api/v1/[0-9A-Fa-f]+/ucc/", handlers.ExternalLinkClickHandler),
    (r"/api/v1/[0-9A-Fa-f]+/nes/", handlers.NotificationEmailSentHandler),
    (r"/api/v1/[0-9A-Fa-f]+/nei/", handlers.NotificationEmailResponseHandler),
]
