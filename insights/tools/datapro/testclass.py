#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
__author__ = 'byouloh'

from datetime import date

class Counter:
    def __init__(self):
        self.number = 0

    # def __call__(self, cls):
    #     return cls

    def incr(self):
        self.number += 1

    def to_dict(self):
        return self.number

        # for key, value in result.iteritems():
        #     try:
        #         result_in = value.to_dict()
        #         result[key] = result_in
        #     except:
        #         return result
        #
        # return result


class GenderGroup:
    def __init__(self, cls):
        genders = ('u', 'f', 'm', 'total')
        self.unknown = cls()
        # print self.unknown
        self.female = cls()
        # print self.female
        self.male = cls()
        self.total = cls()

    def __call__(self):
        return self.__class__

    def incr(self, doc):
        if doc['g'] == 'u':
            self.unknown.incr()
        elif doc['g'] == 'f':
            self.female.incr()
        elif doc['g'] == 'm':
            self.male.incr()
        else:
            print str(doc['_id']) + ': not counted by gender group'
            return False

        self.total.incr()

    def to_dict(self):
        result = self.__dict__

        for key, value in result.iteritems():
            try:
                result_in = value.to_dict()
                result[key] = result_in
            except:
                return result

        return result




class AgeGroup:
    def __init__(self, cls):
        ages = ('0-12', '13-17', '18-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-64', '65+', 'total')
        self._0_12 = cls()
        print '_0_12 : ' + str(self._0_12)
        self._13_17 = cls()
        print self._13_17
        self._18_24 = cls()
        self._25_29 = cls()
        self._30_34 = cls()
        self._35_39 = cls()
        self._40_49 = cls()
        self._50_59 = cls()
        self._60_64 = cls()
        self.gte_65 = cls()
        self.total = cls()

    def __call__(self):
        return self.__class__

    # def __new__(self, cls):
    #     return

    def incr(self, doc):
        age = date.today().year - int(doc['b'].split('/')[0])
        if age >= 0 and age < 13:
            self._0_12.incr(doc)
        elif age >= 13 and age < 18:
            self._13_17.incr(doc)
        elif age >= 18 and age < 25:
            self._18_24.incr(doc)
        elif age >= 25 and age < 30:
            self._25_29.incr(doc)
        elif age >= 30 and age < 35:
            self._30_34.incr(doc)
        elif age >= 35 and age < 40:
            self._35_39.incr(doc)
        elif age >= 40 and age < 50:
            self._40_49.incr(doc)
        elif age >= 50 and age < 60:
            self._50_59.incr(doc)
        elif age >= 60 and age < 65:
            self._60_64.incr(doc)
        elif age >= 65:
            self.gte_65.incr(doc)
        else:
            print str(doc['_id']) + ': not counted by age group'
            return False

        self.total.incr(doc)

    def to_dict(self):
        result = self.__dict__

        for key, value in result.iteritems():
            try:
                result_in = value.to_dict()
                result[key] = result_in
            except:
                return result

        return result


class FriendsGroup:
    def __init__(self, cls):
        friends = ('unknown', '0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'total')
        self.unknown = cls()
        self._0_10 = cls()
        self._11_20 = cls()
        self._21_40 = cls()
        self._41_60 = cls()
        self._61_80 = cls()
        self._81_125 = cls()
        self._126_249 = cls()
        self.gte_250 = cls()
        self.total = cls()

    def __call__(self):
        return self

    def incr(self, doc):
        fc = doc['fc']
        if fc >= 0 and fc < 11:
            self._0_10.incr(doc)
        elif fc >= 11 and fc < 21:
            self._11_20.incr(doc)
        elif fc >= 21 and fc < 41:
            self._21_40.incr(doc)
        elif fc >= 41 and fc < 61:
            self._41_60.incr(doc)
        elif fc >= 61 and fc < 81:
            self._61_80.incr(doc)
        elif fc >= 81 and fc < 126:
            self._81_125.incr(doc)
        elif fc >= 126 and fc < 250:
            self._126_249.incr(doc)
        elif fc >= 250:
            self.gte_250.incr(doc)
        elif fc == 'u':
            self.unknown.incr(doc)
        else:
            print str(doc['_id']) + ': not counted by friends group'
            return False

        self.total.incr(doc)

    def to_dict(self):
        result = self.__dict__

        for key, value in result.iteritems():
            try:
                result_in = value.to_dict()
                result[key] = result_in
            except:
                return result

        return result


class CountryGroup:
    def __init__(self, cls):
        countries = ('Seoul', 'Busan', 'Incheon', 'Jeju', 'Jeonju', 'Daejeon', 'Daegu', 'Pohang', 'Gyeongju',
                    'Jinju', 'Ulsan', 'Chuncheon', 'Anyang', 'Bucheon', 'Cheongju', 'Gumi', 'Gunsan', 'unknown', 'total')

        self.seoul = cls()
        self.busan = cls()
        self.incheon = cls()
        self.jeju = cls()
        self.jeonju = cls()
        self.daejeon = cls()
        self.daegu = cls()
        self.pohang = cls()
        self.gyeongju = cls()
        self.jinju = cls()
        self.ulsan = cls()
        self.chuncheon = cls()
        self.anyang = cls()
        self.bucheon = cls()
        self.cheongju = cls()
        self.gumi = cls()
        self.gunsan = cls()
        self.unknown = cls()
        self.total = cls()

    def __call__(self):
        return self

    def incr(self, doc):
        lc = doc['lc']
        if lc == 'Seoul':
            self.seoul.incr(doc)
        elif lc == 'Busan':
            self.busan.incr(doc)
        elif lc == 'Incheon':
            self.incheon.incr(doc)
        elif lc == 'Jeju':
            self.jeju.incr(doc)
        elif lc == 'Jeonju':
            self.jeonju.incr(doc)
        elif lc == 'Daejeon':
            self.daejeon.incr(doc)
        elif lc == 'Daegu':
            self.daegu.incr(doc)
        elif lc == 'Pohang':
            self.pohang.incr(doc)
        elif lc == 'Gyeongju':
            self.gyeongju.incr(doc)
        elif lc == 'Jinju':
            self.jinju.incr(doc)
        elif lc == 'Ulsan':
            self.ulsan.incr(doc)
        elif lc == 'Chuncheon':
            self.chuncheon.incr(doc)
        elif lc == 'Anyang':
            self.anyang.incr(doc)
        elif lc == 'Bucheon':
            self.bucheon.incr(doc)
        elif lc == 'Cheongju':
            self.cheongju.incr(doc)
        elif lc == 'Gumi':
            self.gumi.incr(doc)
        elif lc == 'Gunsan':
            self.gunsan.incr(doc)
        elif lc == 'unknown':
            self.unknown.incr(doc)
        else:
            print str(doc['_id']) + ': not counted by incrry group'
            return False

        self.total.incr(doc)

    def to_dict(self):
        result = self.__dict__

        for key, value in result.iteritems():
            try:
                result_in = value.to_dict()
                result[key] = result_in
            except:
                return result

        return result


# x = AgeGroup(Counter)
# y = FriendsGroup(x)
# z = CountryGroup(y)
#
# print x.__dict__
# print y.__dict__
# print z.to_dict()
#
# doc = {'g': 'f', 'fc': 220, 'lc': 'Seoul', 'b': '1970/01/10'}
#
# x.incr(doc)

# print 'a is '
# a = GenderGroup(Counter)
#
# # print 'b is '
# # b = FriendsGroup(Counter)
#
# print 'c is '
# c = AgeGroup(Counter)
#
# # print 'd is '
# # d = CountryGroup(Counter)
#
# print 'x is '
# x = AgeGroup(GenderGroup(Counter))
#
# print 'y is '
# y = GenderGroup(AgeGroup(Counter)) #(FriendsGroup(Counter)))
#
# # print 'z is '
# # z = CountryGroup(GenderGroup(AgeGroup(FriendsGroup(Counter))))
#
# print y.to_dict()

# print z.to_dict()

from collections import defaultdict

class A:
    gender = ['m', 'f', 'u', 't']
    ages = ['0-12', '13-17', '18-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-64', '65+', 't']
    friends = ['0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'u', 't']
    country = ['Seoul', 'Busan', 'Incheon', 'Jeju', 'Jeonju', 'Daejeon', 'Daegu', 'Pohang', 'Gyeongju',
           'Jinju', 'Ulsan', 'Chuncheon', 'Anyang', 'Bucheon', 'Cheongju', 'Gumi', 'Gunsan', 'u', 't']

    all_params = {
            'g': gender,
            'lc': country,
            'f': friends,
            'a': ages
        }

    params = dict()

    def __init__(self, *arg):
        for key in arg:
            if key in self.all_params.keys():
                self.params[key] = self.all_params[key]

        self.groups = eval(self.datamesh(self.params.keys()))

        self.arg = list(arg)

        print self.datamesh(self.params.keys())
        print self.groups
        print self.params


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


    def classify_ages(self, doc):
        age = date.today().year - int(doc['b'].split('/')[0])

        for i in self.ages:
            if '-' in self.ages[i]:
                segment = self.ages[i].split('-')
                start = int(segment[0])
                end = int(segment[1])
                print segment
                if age >= start and age <= end:
                    return self.ages[i]

            elif '+' in self.ages[i]:
                segment = self.ages[i].split('+')
                if age >= segment[0]:
                    return self.ages[i]

            elif self.ages[i] == 'u':
                return self.ages[i]
            elif self.ages[i] == 't':
                return self.ages[i]
            else:
                print str(doc['_id']) + ': not counted by age group'
                return None


def to_dict(x):
        return dict(
            (k, to_dict(v))
            for (k, v) in x.iteritems()
        ) if isinstance(x, defaultdict) else x

def anothertodict(self):
    stuff = dict(self)
    for (key, val) in stuff.iteritems():
        if isinstance(val, defaultdict):
            stuff[key] = val.anothertodict()
    return stuff

class B:


    def __init__(self, arg):
        self.var = arg

class C:


    def __init__(self, arg):
        self.var = arg

class D:


    def __init__(self, arg):
        self.var = arg

a = A('a', 'g', 'f', 'lc')
#
# friends = ['0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'u', 't']
# country = ['Seoul', 'Busan', 'Incheon', 'Jeju', 'Jeonju', 'Daejeon', 'Daegu', 'Pohang', 'Gyeongju',
#        'Jinju', 'Ulsan', 'Chuncheon', 'Anyang', 'Bucheon', 'Cheongju', 'Gumi', 'Gunsan', 'u', 't']
#
a.groups[u'30s'][u'total']['21-40']['Anyang'] += 1 #['21-40']['Anyang']
print 'first insert complete'
print a.groups
print a.to_dict(a.groups)

a.groups['20s']['f']['61-80']['Daejeon'] += 1 #['61-80']['Daejeon']
a.groups['30s']['m']['61-80']['Daejeon'] += 1
a.groups['30s']['f']['21-40']['Anyang'] += 1
a.groups['30s']['f']['21-40']['Daejeon'] += 1
a.groups['10s']['f']['21-40']['Daejeon'] += 1
print 'second insert complete'
print a.groups
print a.to_dict(a.groups)


b = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda :defaultdict(int))))


x = ('a', 'b', 'c', 'd')
print x

y = list(x)
print y

#
# b[u'30s'][u'total']['21-40']['Anyang'] += 1 #['21-40']['Anyang']
# print 'first insert complete'
# print b
# print to_dict(b)
#
# b['20s']['f']['61-80']['Daejeon'] += 1 #['61-80']['Daejeon']
# b['30s']['f']['21-40']['Anyang'] += 1
# b['30s']['f']['21-40']['Daejeon'] += 1
# b['10s']['f']['21-40']['Daejeon'] += 1
# print 'second insert complete'
# print b
# print to_dict(b)

# a.groups['20s']['total'] += 1
# print a.groups
#
# a.groups['30s']['m'] += 1
# a.groups['30s']['f'] += 1
# print a.groups
# a.groups['30s']['total'] += 1
# a.groups['30s']['m'] += 1
# a.groups['30s']['f'] += 1
# print a.groups
#
# a.groups['20s']['m'] += 1
# print a.groups
# # a.groups['f']['f'] = a.groups['f']['f'] + 1
# # a.groups['g']['f']['lc']['a']['total'] = 1
# # a.groups['lc']['total'] += 1
#
# print a.groups
#
# print a.to_dict(a.groups)


#
# # a.dic['u'] += 1
# print a.__class__
# print a.dic
#
# print a.__dict__
# print A
# print a.group_params

# x = {'a':1, 'b':2}
# y = dict({'x': x})
# z = dict({'y': y})
# print x
# print y
# print z
#
#
#
#
# # b = dict(dict(dict()))
# # print b
# #
# #
# def c():
#  return defaultdict(lambda: defaultdict(int))
#
# print c
#
# d = defaultdict(c)
# print d
#
# d[0][1][2] = 2
#
# print d
# print d.items()
# print d.default_factory
#
# d.default_factory = None
#
# print d.default_factory
# print d.items()
#
# d = to_dict(d)
# print d
#
#
# e = defaultdict(lambda :defaultdict(int))
#
# e['a'] = 1
# e['b']['c'] = 2
#
# print e
# print e.items()
# print e.default_factory
#
# e.default_factory = None
#
# print e.default_factory
# print e.items()
#
#
# def todict(self):
#     for (key, val) in self.iteritems():
#         if isinstance(val, defaultdict):
#             val.todict()
#             self[key] = dict(val)
#     self = dict(self)
#
#
#
# e = to_dict(e)
#
# print e
#
#
#
# # for value in e.items().
# # if isinstance(e.items(), defaultdict):
# #     pass
#
#
# import random
#
# # class DefaultGroup(dict):
# #     '''Implementation of perl's autovivification feature.'''
# #     def __getitem__(self, item):
# #         try:
# #             return dict.__getitem__(self, item)
# #         except KeyError:
# #             print 'type is ' + type(self)
# #             self[item] = type(self)()
# #             return self[item]
# #
# def tree():
#     return defaultdict(tree)
#
#
# a = tree()
#
# print a
#
# gender = ('m', 'f', 'u', 'total')
# ages = ('0-12', '13-17', '18-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-64', '65+', 'total')
# friends = ('unknown', '0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'total')
# country = ('Seoul', 'Busan', 'Incheon', 'Jeju', 'Jeonju', 'Daejeon', 'Daegu', 'Pohang', 'Gyeongju',
#            'Jinju', 'Ulsan', 'Chuncheon', 'Anyang', 'Bucheon', 'Cheongju', 'Gumi', 'Gunsan', 'unknown', 'total')
#
# for i in gender:
#     for j in ages:
#         for k in friends:
#             for l in country:
#                 value = random.randint(0, 1)
#                 if value == 1:
#                     a[i][j][k][l] = 1
#                 if isinstance(a[i][j][k][l], int):
#                     a[i][j][k][l] += 1
#                 else:
#                     a[i][j][k][l] = 0
#
# # a['f'] = {}
# # a['f']['g'] = 1
#
# print a
# print a.items()
#
# a = to_dict(a)
#
# print a
# print a.items()
#
#

