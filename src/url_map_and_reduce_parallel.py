from datetime import date


def days_between(start, stop):
    # Create a generator for yielding days between start and stop dates.
    today = date(*start)
    stop = date(*stop)

    while today < stop:
        datestr = today.strftime("%m-%d-%Y")
        yield "http://jtwolohan.com/arch-rival-blog/" + datestr
        today = date.fromordinal(today.toordinal() + 1)


date_gen = days_between(start=(2001, 1, 1), stop=(2002, 12, 31))

import requests


def get_url(path):
    # Return the HTML of a webpage as bytes
    return requests.get(path).content

import os
from multiprocessing import Pool

with Pool(processes=os.cpu_count()) as pool:
    blog_posts = pool.map(get_url, date_gen)
    blog_posts = list(blog_posts)

with Pool(processes=4) as pool:
    pool.map(print, range(20))

def print_and_return(x):
    print(x)
    return x

with Pool(processes=4) as pool:
    result = pool.map(print_and_return, range(20))