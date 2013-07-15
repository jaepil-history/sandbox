data = {'10': {'a': 2, 'c': 3}, '20': {'a': 3, 'b': 4}, '30': {'b': 5, 'd': 1}}

param = ['a', 'b', 'c', 'd', 't']
grand_total = {}

for key in param:
    grand_total[key] = 0

for sub_dict in data.values():
    subtotal = 0
    for value in sub_dict.values():
        subtotal += value
        sub_dict['t'] = subtotal
        for key in grand_total.keys():
            if sub_dict.has_key(key):
                grand_total[key] += sub_dict[key]

data['t'] = grand_total

print data

import numpy as np

gender = ['m', 'f', 'u', 't']
ages = ['0-12', '13-17', '18-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-64', '65+', 't']
friends = ['0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'u', 't']
country = ['Seoul', 'Busan', 'Incheon', 'Jeju', 'Jeonju', 'Daejeon', 'Daegu', 'Pohang', 'Gyeongju',
           'Jinju', 'Ulsan', 'Chuncheon', 'Anyang', 'Bucheon', 'Cheongju', 'Gumi', 'Gunsan', 'u', 't']

data = np.matrix('1 2; 3 4')

print data

a = np.array(data).tolist()

print 'a: ' + str(a)

a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = np.array(a)
print b

c = np.array(b).tolist()
print 'c: ' + str(c)



x = np.matrix(np.arange(12).reshape((3,4)))
print x

print sum(x)

y = [0, 1, 2, 4]
y.append(sum(y))

print y

# matrix([[ 0,  1,  2,  3],
#         [ 4,  5,  6,  7],
#         [ 8,  9, 10, 11]])

_x = np.array(x).tolist()
print _x

print

print '======'

y = x[0];
print y
# matrix([[0, 1, 2, 3]])

print (x == y)
# matrix([[ True,  True,  True,  True],
#         [False, False, False, False],
#         [False, False, False, False]], dtype=bool)

print (x == y).all()
# False

print (x == y).all(0)
# matrix([[False, False, False, False]], dtype=bool)

print (x == y).all(1)
# matrix([[ True],
#         [False],
#         [False]], dtype=bool)

m = np.matrix([1,2,3])
print m



l = np.array(m).flat
print l

l = np.array(m).flatten().tolist()
print l
