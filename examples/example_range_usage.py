#!/usr/bin/env python

from openrange import Range

def range_demo():

    for n in Range(.5, 3.5, .25):
        print str(n) 

if __name__ == "__main__":
    range_demo() 

