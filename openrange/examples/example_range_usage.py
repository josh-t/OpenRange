#!/usr/bin/env python

from __future__ import print_function
from openrange import Range

if __name__ == "__main__":

    for i in Range(10):
        print(i, end=" ")
    print()

    for i in Range(0, 5):
        print(i, end=" ")
    print()

