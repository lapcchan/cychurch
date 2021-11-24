#-* - coding: utf-8 -*-

#ordered dict
from UserDict import UserDict

class odict(UserDict):
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)
#end of ordered dict


#!/usr/bin/python
#-* - coding: utf-8 -*-
# integer number to word conversion

num = ["", "壹","貳","叁","肆","伍","陸","柒","捌","玖","拾"]


def int2word(n):
    """
    convert an integer number n into a string of words
    """
    n = int(n)
    result = ""
    ten = False
    ntmp = n
    if n > 9999999:
        tmp = ntmp/10000000
        ntmp = ntmp - (tmp*10000000) 
        if tmp > 0: result += num[tmp] + "仟"
    if n > 999999:
        tmp = ntmp/1000000
        ntmp = ntmp - (tmp*1000000) 
        if tmp > 0: result += num[tmp] + "佰"
    if n > 99999:
        tmp = ntmp/100000
        ntmp = ntmp - (tmp*100000) 
        if tmp > 0: result += num[tmp] + "拾"
    if n > 9999:
        tmp = ntmp/10000
        ntmp = ntmp - (tmp*10000) 
        if tmp > 0: result += num[tmp] + "萬"
        elif n > 9999: result += "萬"
    if n > 999:
        tmp = ntmp/1000
        ntmp = ntmp - (tmp*1000) 
        if tmp > 0: result += num[tmp] + "仟"
    if n > 99:
        tmp = ntmp/100
        ntmp = ntmp - (tmp*100) 
        if tmp > 0: result += num[tmp] + "佰"
    if n > 9:
        tmp = ntmp/10
        ntmp = ntmp - (tmp*10) 
        if tmp > 0: 
            result += num[tmp] + "拾"
            ten = True
    if n > 0:
       if ntmp > 0:
           if not ten and n > 9 :
               result += "零"
           result += num[ntmp]


    result += "元正"

    return result 

if __name__ == '__main__':
    n = 43210
    print n
    print "-"*50
    print int2word(n)
    print "-"*50
    print 1, int2word(1)
    print 4, int2word(4)
    print 10, int2word(10)
    print 11, int2word(11)
    print 34, int2word(34)
    print 101, int2word(101)
    print 131, int2word(131)
    print 50301, int2word(50301)
    print 79804, int2word(79804)
    print 100000.01, int2word(100000.01)
    print 100000,int2word(100000)
    print 456789, int2word(456789)
    print 3234567, int2word(3234567)
    print 3000300, int2word(3000300)
    print 83456322, int2word(83456322)
    print 83000300, int2word(83000300)
