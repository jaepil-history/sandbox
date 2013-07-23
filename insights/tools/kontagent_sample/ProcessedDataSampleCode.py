__author__ = 'byouloh'

import urllib2, base64, json, csv

url =('http://query.kontagent.net/processed/v1/social/users/uniques/series.json/?'
      'api_key=123abc4def5a6bc7890d12e34f5a6789&'
      'time_segment=day&'
      'start_time=20111001_0000&'
      'end_time=20111101_0000')
countries = ['US', 'CA']
username = 'you@your_company.com'
password = 'secret_password'

all_data = {}
dates = set()

base64string = base64.encodestring("%s:%s" % (username, password))[:-1]
authheader = 'Basic %s' % base64string

for country in countries:
    all_data[country] = {}
    req = urllib2.Request(url + '&country=%s' % country)
    req.add_header('Authorization', authheader)
    handle = urllib2.urlopen(req)
    data = handle.read()
    tmp_list = json.loads(data)

    for i in tmp_list:
        dates.add(i[0])
        all_data[country][i[0]] = i[1]

        dates = sorted(list(dates))
dataWriter = csv.writer(open('demo1.csv', 'wb'))
dates.insert(0, 'Date')
dataWriter.writerow(dates)

for country, v in all_data.iteritems():
    cnt = v.values()
    cnt.insert(0, country)
    dataWriter.writerow(cnt)