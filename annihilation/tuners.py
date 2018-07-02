from pytils.translit import slugify as pyslugify
from datetime import datetime as python_datetime


def slugify(value):
    # important: value arg must be last
    return pyslugify(value)


def default(default_value, value):
    return value or default_value


def slice(opt, value):
    left, right = map(int, opt.split(','))
    return value[left:right]


def datetime(format, value):
    return python_datetime.strptime(value, format)
