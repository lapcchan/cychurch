#!/usr/bin/python25
# -*- coding: utf-8 -*-

# 32space 44, 46. 59; 41) 93] 47/ 92\ 10\n 64@

def _swap(s):
    h = u""
    for i in range(len(s)):
        if (ord(s[i]) >= 128) or (ord(s[i]) in [32,44,46,47,92,59,10,64]):
            if len(h) > 0:
                #print "debug h > 0, %s" % s[i]
                yield h
                h = u""
            yield s[i]
        else:
            #print "english, this:%s, total:%s" % (s[i],h)
            h += s[i]
    if len(h) > 0: yield h

def swap(s,total=1,ascii_size=1):
    count = 0
    h = u""
    for c in _swap(s):
        if len(c) == 1 and (ord(c) >= 128): thiscount = 2
        elif len(c) == 1: thiscount = ascii_size
        else: thiscount = len(c)*ascii_size
        count += thiscount
        if len(c) == 1 and ord(c) == 10:
            if len(h) > 0: yield h
            else: yield u"\n"
            h = u""
            count = 0
        elif count > total:
            if len(h) > 0: yield h
            count = thiscount
            h = c
        else:
            h += c
    if len(h) > 0: yield h

def linecount(s,word=1):
    count = 0;
    for x in swap(s,word):
        count += 1
    return count

if __name__=="__main__":

    teststring = "hello\n this is english,and this, is chinese筆劃,打,中風,撫,摩\n衝程劃尾槳撫摩劃去筆劃a"
    uu = teststring.decode('utf-8')
    for x in swap(uu,20):
        print x
    print linecount(uu,20)
