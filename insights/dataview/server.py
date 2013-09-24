import os.path
import base64

import tornado.web

from dataview.views.app import(
        MainView,
        IndexView,
        BasicView,
        AnalyticsView,
        OperationView,
        DashboardView,
        SettingsView,
        SettingsChangePasswordView)
from dataview.views.auth import LoginView, CreateUserView, LogoutView
from dataview.defaults import PROJECT_ROOT
from dataview.config import settings


login_url = "{0}:{1}/login".format(settings.WEB_APP['host'], settings.WEB_APP['port'])\
    if settings.PROXY is None else '/login'
    
app_settings = {
	"static_path": os.path.join(PROJECT_ROOT, "media"),
	"cookie_secret": base64.b64encode(settings.SECRET_KEY),
	"login_url" : login_url,
	"session": {"duration": 3600, "regeneration_interval": 240, "domain": settings.WEB_APP['host']}
}

handlers = [
	# App
    (r"/", MainView),
    (r"/index", IndexView),
    (r"/basic", BasicView),
    (r"/analytics", AnalyticsView),
    (r"/operation", OperationView),
	(r"^/settings", SettingsView),
    (r"^/settings/change-password$", SettingsChangePasswordView),
	# Auth
	(r"/login", LoginView),
	(r"/logout", LogoutView),
	(r"/create_user", CreateUserView),
	# Static
	(r"/media/(.*)", tornado.web.StaticFileHandler, {"path": app_settings['static_path']})
]

application = tornado.web.Application(handlers, **app_settings)


if __name__ == "__main__":
    application.listen(int(settings.WEB_APP['port']))
    tornado.ioloop.IOLoop.instance().start()