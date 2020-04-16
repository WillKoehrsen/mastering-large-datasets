from datetime import date


def days_between(start, stop):
    # Create a generator for yielding days between start and stop dates.
    today = date(*start)
    stop = date(*stop)

    while today < stop:
        datestr = today.strftime("%m-%d-%Y")
        yield "http://jtwolohan.com/arch-rival-blog/" + datestr
        today = date.fromordinal(today.toordinal() + 1)


date_gen = days_between(start=(2001, 1, 1), stop=(2010, 12, 31))

import requests


def get_url(path):
    # Return the HTML of a webpage as bytes
    return requests.get(path).content

blog_posts = map(get_url, date_gen)