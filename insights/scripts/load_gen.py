import random
import sys

import tornado.httpclient
import tornado.httputil
import tornado.options


class InsightsClient(object):
    INSIGHTS_API_URL = "http://api.insights.appspand.com:8001/api/v1/"

    def __init__(self, app_id):
        self.app_id = app_id

    def make_request(self, app_id, message_type, params):
        url = self.INSIGHTS_API_URL
        url += app_id + "/" + message_type + "/?"
        url += tornado.httputil.urlencode(params)

        return url

    def send_request(self, url):
        client = tornado.httpclient.HTTPClient()
        try:
            client.fetch(url)
        except tornado.httpclient.HTTPError as e:
            print "Error:", e
        client.close()

    def track_apa(self, uuid):
        params = {
            "uuid": uuid
        }

        url = self.make_request(self.app_id, "apa", params)
        self.send_request(url)

    def track_apr(self, uuid):
        params = {
            "uuid": uuid
        }

        url = self.make_request(self.app_id, "apr", params)
        self.send_request(url)

    def track_cpu(self, uuid):
        birthday = ["%04d" % random.randint(1900, 2000),
                    "%02d" % random.randint(1, 12),
                    "%02d" % random.randint(1, 28)]
        gender = ["m", "f", "u"]
        country = ["Seoul", "Busan", "Incheon", "Jeju", "Jeonju", "Daejeon", "Daegu", "Pohang", "Gyeongju",
                   "Jinju", "Ulsan", "Chuncheon", "Anyang", "Bucheon", "Cheongju", "Gumi", "Gunsan"]

        params = {
            "uuid": uuid,
            "b": "/".join(birthday),
            "g": gender[random.randint(0, 2)],
            "lc": country[random.randint(0, 16)],
            "f": random.randint(0, 1000)
        }

        url = self.make_request(self.app_id, "cpu", params)
        self.send_request(url)

    def track_evt(self):
        pass

    def track_ins(self):
        pass

    def track_inr(self):
        pass

    def track_gci(self):
        pass

    def track_mtu(self, uuid):
        params = {
            "uuid": uuid
        }

        url = self.make_request(self.app_id, "mtu", params)
        self.send_request(url)

    def track_pgr(self, uuid):
        params = {
            "uuid": uuid
        }

        url = self.make_request(self.app_id, "pgr", params)
        self.send_request(url)

    def track_pst(self):
        pass

    def track_psr(self):
        pass

    def track_ucc(self):
        pass

    def track_nes(self):
        pass

    def track_nei(self):
        pass


def main(args):
    if len(args) < 2:
        print "load_gen.py [App ID]"
        return

    app_id = args[1]

    client = InsightsClient(app_id=app_id)

    for uuid in range(10000, 12000):
        client.track_apa(uuid)
        client.track_pgr(uuid)
        client.track_cpu(uuid)
        client.track_pgr(uuid)
        #client.track_mtu(uuid)


if __name__ == "__main__":
    main(sys.argv)
