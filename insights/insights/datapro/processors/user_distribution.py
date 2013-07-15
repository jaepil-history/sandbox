#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand


'''
app_id.cpu schema
{
    lc: ["Seoul", "Busan", "Incheon", "Jeju", "Jeonju", "Daejeon", "Daegu", "Pohang", "Gyeongju",
                   "Jinju", "Ulsan", "Chuncheon", "Anyang", "Bucheon", "Cheongju", "Gumi", "Gunsan"], # local country
    b: 'xxxx/xx/xx',    # birthday
    g: {f, m, u},       # gender
    f: int,             # friends count
    _mt: ,
    _dt: ,
    ts: ,
    _id: ,
    uuid: ,
    data: ,             # acount information {id, email, password}
}
'''
'''
app_id.processed schema
{
    title: user distribution
    order: {'g', 'f', 'a', 'lc'}  # group order. from right to left
    runtime: ms
    count: the number of handled data
    last_id: the last handled doc's id
    result: processed data
    ts: timestamp
}
'''

from pymongo import MongoClient
import settings

from datetime import datetime, date
import time

from collections import defaultdict


options = settings.parse_options()

db_client_processed = MongoClient(host=options.mongodb_processed_connection_uri,
                            max_pool_size=options.mongodb_max_concurrent)
db_processed = db_client_processed[options.mongodb_processed_db_name]

db_client_appspand = MongoClient(host=options.mongodb_appspand_connection_uri,
                            max_pool_size=options.mongodb_max_concurrent)
db_appspand = db_client_appspand[options.mongodb_appspand_db_name]
col_application = db_appspand.application

apps = list(col_application.find())
# print apps

def open_db_clients(connection_uri, db_name):
    db_client = MongoClient(host=connection_uri)
    db = db_client[db_name]
    return db

insights_dbs = []

for app in apps:
    temp = {}
    temp['app_id'] = str(app['_id'])
    temp['cluster_name'] = app['cluster']['name']
    temp['db_name'] = app['cluster']['db_name']
    temp['app_name'] = app['name']
    temp['db'] = open_db_clients("mongodb://localhost:27017", app['cluster']['db_name'])
    insights_dbs.append(temp)

# print insights_dbs


class Groups:
    gender = ['m', 'f', 'u', 't']
    ages = ['0-12', '13-17', '18-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-64', '65+', 't']
    friends = ['0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'u', 't']
    country = ['Seoul', 'Busan', 'Incheon', 'Jeju', 'Jeonju', 'Daejeon', 'Daegu', 'Pohang', 'Gyeongju',
           'Jinju', 'Ulsan', 'Chuncheon', 'Anyang', 'Bucheon', 'Cheongju', 'Gumi', 'Gunsan', 'u', 't']

    params = {
            'g': gender,
            'lc': country,
            'f': friends,
            'a': ages
        }

    def __init__(self, *arg):
        for key in arg:
            if key not in self.params.keys():
                print key + ': argument is not in predefined parameters, ' + str(self.params.keys())
                return False

        self.args = list(arg)
        code = compile(self.datamesh(self.args), '<string>', 'eval')
        self.groups = eval(code)
        self.args = list(arg)

        self.count_code = None
        self.count_code = self.make_count_code(self.args)


    """
      재귀호출로 arg의 순서대로 호출되며,
      최종함수는 int형 value를 가지는 defaultdict(int)으로 선언된다.
      ex) arg = ('g', 'f', 'lc) 이면,
      gender별, friends별, country별 분류이며
      data type은 defaultdict(lambda: defaultdict(lambda: defaultdict(int)))로
      {'gender_key': {'friends_key': {'country_key': 1}}}의 형태로 데이타가 저장되도록 해야한다.
    """
    def datamesh(self, keys):
        if len(keys) < 2:
            return 'defaultdict(int)'
        else:
            keys.pop(0)
            return 'defaultdict(lambda:' + self.datamesh(keys) + ')'


    def to_dict(self, x):
        return dict(
            (k, self.to_dict(v))
            for (k, v) in x.iteritems()
        ) if isinstance(x, defaultdict) else x


    # total 제외. 차원이 늘수록 *2 배씩 total element가 증가. 추후 고려
    def make_count_code(self, args):
        code = 'self.groups'
        for key in args:
            if key == 'g':
                code += '[' + 'doc[' + '\'' + 'g' + '\'' + ']' + ']'
            elif key == 'lc':
                code += '[' + 'doc[' + '\'' + 'lc' + '\'' + ']' + ']'
            elif key == 'a':
                code += '[' + 'self.classify(doc,' + '\'' + 'a' + '\'' + ',' + 'self.ages' + ')' + ']'
            elif key == 'f':
                code += '[' + 'self.classify(doc,' + '\'' + 'f' + '\'' + ',' + 'self.friends' + ')' + ']'
            else:
                print key + ' group not in the predefined groups'
                return False

        code += ' += 1'
        #print code
        return compile(code, '<string>', 'exec')

    def count(self, doc):
        if self.count_code is not None:
            exec self.count_code
        else:
            print 'Error: self.count_code is None'
            return False

    def classify(self, doc, arg, arr):
        if arg == 'a':
            position = date.today().year - int(doc['b'].split('/')[0])
        elif arg == 'f':
            position = doc['f']
        else:
            print arg + ' is not predefined'

        for value in arr:
            if '-' in value:
                segment = value.split('-')
                start = int(segment[0])
                end = int(segment[1])
                if position >= start and position <= end:
                    return value

            elif '+' in value:
                segment = value.split('+')
                if position >= int(segment[0]):
                    return value

            elif value == 'u':
                return value
            elif value == 't':
                return value
            else:
                print str(doc['_id']) + ': not counted by ' + arg + ' group'
                return None


result = dict()

for app in insights_dbs:
    counter = Groups('lc', 'f', 'a', 'g')
    col_cpu_name = app['app_id'] + '.event.cpu'
    col_processed_name = app['app_id'] + '.processed'
    db = app['db']
    col_cpu = db[col_cpu_name]

    count = 0
    elapsed = 0
    last_doc_id = 0
    start = time.time()

    for doc in col_cpu.find():
        count = count + 1
        counter.count(doc)

    end = time.time()

    elapsed = (end - start) * 1000
    print 'time to read db: ' + str(elapsed) + 'msec'
    print 'counted items: ' + str(count)

    temp = {}
    ts = datetime.utcnow()
    print ts
    temp['title'] = 'user_distribution'
    temp['order'] = counter.args
    temp['runtime'] = elapsed
    temp['count'] = count
    temp['last_id'] = last_doc_id
    temp['ts'] = ts
    print 'counted order: ' + str(counter.args)
    counter = counter.to_dict(counter.groups)
    temp['result'] = counter
    result[col_processed_name] = temp


# print counter.total.total.total.total

start = time.time()
for key, value in result.iteritems():
    # print key
    # print value.__dict__
    col_processed = db_processed[key]
    col_processed.insert(value)

end = time.time()

elapsed = str((end - start)) + 'sec'
print 'time to write: ' + elapsed

# print 'counter total: ' + counter['t']['t']['t']['t']

# print



print '--------------------------------------------------------------'
# print counter.to_dict()
print '--------------------------------------------------------------'
# print counter.total.to_dict()
print '--------------------------------------------------------------'
# print counter.total.total.to_dict()
print '--------------------------------------------------------------'
# print counter.total.total.total.to_dict()
# print counter.total.total.total.total.to_dict()


# print counter.total.total.total.female
# print counter.total.total.total.male
# print counter.total.total.total.unknown
#
#
# print counter.total._11_20.total.total
# print counter.total._11_20._18_24.female
#
# print counter.total.total.gte_65.total
#
# print counter.total.total._0_12.total
#
# print counter.total._21_40.total.total
# print counter.total._21_40.total.female
# print counter.total._21_40.total.male
# print counter.total._21_40.total.unknown
#
# print counter.seoul.total.total.female
# print counter.seoul.total.total.male
# print counter.seoul.total.total.unknown
# print counter.seoul.total.total.total

