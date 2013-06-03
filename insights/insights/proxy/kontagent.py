import tornado.escape
import tornado.httpclient


class Kontagent(object):
    def __init__(self, app_id, use_https=False, use_test_server=False):
        self.app_id = app_id

        if use_https is True:
            self.server_url = "https://"
        else:
            self.server_url = "http://"

        if use_test_server is True:
            self.server_url += "test-server.kontagent.com"
        else:
            self.server_url += "api.geo.kontagent.net"

        self.server_url += "/api/v1/" + self.app_id + "/"

        self.field_names = {
            "uuid": "s",
            "tuid": "u",
            "suid": "su",
            "lv": "l",
            "data": "data",
            "ts": "ts"
        }

    def build_url(self, message_type, **arguments):
        count = 0
        params = str()
        for k, v in arguments.items():
            if count > 0:
                params += "&"
            if k in self.field_names:
                k = self.field_names[k]
            params += (k + "=" + tornado.escape.url_escape(v))
        return self.server_url + message_type + "/?" + params

    def send_request(self, message_type, **arguments):
        request_url = self.build_url(message_type, **arguments)
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch(request_url, callback=self.on_completed)

    def on_completed(self, response):
        print response.body

    def track_application_added(self, **arguments):
        self.send_request(message_type="apa", **arguments)

    def track_application_removed(self, **arguments):
        self.send_request(message_type="apr", **arguments)

    def track_user_information(self, **arguments):
        self.send_request(message_type="cpu", **arguments)

    def track_custom_event(self, **arguments):
        self.send_request(message_type="evt", **arguments)

    def track_invite_sent(self, **arguments):
        self.send_request(message_type="ins", **arguments)

    def track_invite_received(self, **arguments):
        self.send_request(message_type="inr", **arguments)

    def track_goal_counts(self, **arguments):
        self.send_request(message_type="gci", **arguments)

    def track_revenue(self, **arguments):
        self.send_request(message_type="mtu", **arguments)

    def track_page_request(self, **arguments):
        self.send_request(message_type="pgr", **arguments)

    def track_stream_post(self, **arguments):
        self.send_request(message_type="pst", **arguments)

    def track_stream_response(self, **arguments):
        self.send_request(message_type="psr", **arguments)

    def track_external_link_click(self, **arguments):
        self.send_request(message_type="ucc", **arguments)

    def track_notification_email_sent(self, **arguments):
        self.send_request(message_type="nes", **arguments)

    def track_notification_email_response(self, **arguments):
        self.send_request(message_type="nei", **arguments)
