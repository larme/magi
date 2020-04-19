from datetime import datetime, date, timedelta
from dateutil import relativedelta
import calendar

ONEDAY = timedelta(days=1)
ONEMONTH = ONEDAY * 30

# Symbol meanings in function name:
# dt: datetime.datetime object
# date: usually a datetime.datetime object representing a date e.g. (datetime(2015, 11, 8, 0, 0)), sometimes it also means the datetime.date object
# date_str: '2015-11-08' or '2015/11/08'
# date_range_str: '2015-11-01--2015-11-08' or '2015/11/01--2015/11/08', both ends are inclusive

def iso_year_start(iso_year):
    """The gregorian calendar date of the first day of the given ISO year"""
    fourth_jan = date(iso_year, 1, 4)
    delta = timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta

def iso_to_gregorian(iso_year, iso_week, iso_day):
    """Gregorian calendar date for the given ISO year, week and day"""
    year_start = iso_year_start(iso_year)
    return year_start + timedelta(days=iso_day-1, weeks=iso_week-1)


def dt_to_date_str(dt):
    return str(dt.date())

def parse_date_str(date_str):
    """parse a date string in 2015-08-01 or 2015/08/01 format to datetime"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y/%m/%d')
        except ValueError:
            raise ValueError("%s is not a date string" % date_str)

def dt2date(dt):
    return dt.date()

def date2dt(date):
    return parse_date_str(str(date))

def any2dt(obj):
    """convert datetime, date or date_str to datetime object"""
    if isinstance(obj, datetime):
        return obj
    elif isinstance(obj, date):
        return date2dt(date)
    elif isinstance(obj, basestring):
        return parse_date_str(obj)
    else:
        raise TypeError("Cannot convert %s into datetime object" % obj)

def any2date(obj):
    """convert datetime, date or date_str to date object"""
    if type(obj) == date:
        return obj

    return any2dt(obj).date()

def any2date_str(obj):
    """convert datetime, date or date_str to date_str"""
    if isinstance(obj, basestring):
        return obj

    return str(any2date(obj))

def normalize_date_str(date_str):
    """normalize date string to 0000-00-00 format"""
    return any2date_str(any2date(date_str))

def parse_date_range_str(date_range_str):
    """parse a date string in "2015-10-08--2015-10-10" format to two datetime objects

    Return [date1, date2]
    If the given string is in "2015-10-10" format, then return [date1, date1]"""

    date_strs = date_range_str.split('--')

    if len(date_strs) == 1:
        date_strs *= 2

    dates = [parse_date_str(date_str) for date_str in date_strs]
    return dates

def date_range(start, end, freq=None):
    """Generate date range from start to end

    Freq is in integer."""

    import pandas as pd

    if freq is None:
        dr = pd.date_range(start, end)
    else:
        dr = pd.date_range(start, end, "%dD")

    return [dt.date() for dt in dr.tolist()]

def date_str_range(start, end, freq=None):
    dates = date_range(start, end, freq)
    date_strs = [str(date) for date in dates]
    return date_strs

def date_range_str_to_dates(date_str, freq=None):
    """gen dates from '2015-10-28--2015-11-08' to dates"""
    start, end = parse_date_range_str(date_str)
    return date_range(start, end, freq)

def date_range_str_to_date_strs(date_str, freq=None):
    """gen date_strs from string like '2015-10-28--2015-11-08' to '2015-10-28'..."""
    start, end = parse_date_range_str(date_str)
    return date_str_range(date_start, end, freq)

def date_range_str_to_start_and_end(date_range_str):
    ts = date_range_str.split('--')
    if len(ts) == 1:
        start = ts[0]
        end = start

    elif len(ts) == 2:
        start, end = ts

    else:
        return

    return start, end

def date_str_add_days(date_str, days):
    """add days (in int) to a date_str

    For example date_str_add_days('2015-08-13', 3) => '2015-08-16' """
    date = parse_date_str(date_str)
    delta = timedelta(days=days)
    ret_dt = date + delta
    return dt_to_date_str(ret_dt)
    
def last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

def this_monday(date_obj=None):
    if not date_obj:
        date_obj = str(datetime.today().date())
    dt = any2dt(date_obj)
    weekday = dt.weekday()
    delta = timedelta(days=weekday)
    return str((dt - delta).date())

def gen_today_date_str():
    return str(datetime.today().date())

def gen_yesterday_date_str():
    return date_str_add_days(gen_today_date_str(), -1)

def gen_tomorrow_date_str():
    return date_str_add_days(gen_today_date_str(), 1)

def gen_date_range_str(start_date, end_date):
    return "%s--%s" % (str(start_date), str(end_date))

def gen_week_date_range_str(year, week):
    first_day = iso_to_gregorian(year, week, 1)
    last_day = iso_to_gregorian(year, week, 7)
    return gen_date_range_str(first_day, last_day)

def gen_last_week_date_range_str(today=None):
    if today:
        today = any2dt(today)
    else:
        today = datetime.today()

    last_week_day = today - timedelta(days=7)
    year, week, _ = last_week_day.isocalendar()
    return gen_week_date_range_str(year, week)

def gen_month_date_range_str(year, month):
    first_day = datetime(year, month, 1).date()
    last_day = datetime(year, month, last_day_of_month(year, month)).date()
    return gen_date_range_str(first_day, last_day)

def gen_month_date_range_strs(year, months):
    return [gen_month_date_range_str(year, month) for month in months]

def month_range(start, end):
    ret = []
    if start > end:
        return ret
    start_year, start_month = start
    start_date = datetime(start_year, start_month, 1)
    end_year, end_month = end
    end_date = datetime(end_year, end_month, 1)

    ret.append((start_year, start_month))
    while start_date != end_date:
        next_month_of_start_date = start_date + relativedelta.relativedelta(months=1)
        year = next_month_of_start_date.year
        month = next_month_of_start_date.month
        ret.append((year, month))
        start_date = next_month_of_start_date

    return ret

def gen_month_range_date_range_strs(start, end):
    return [gen_month_date_range_str(year, month)
            for year, month in month_range(start, end)]

def date_range_str_to_date_strs(date_str):
    start, end = parse_date_range_str(date_str)
    return date_str_range(start, end)

def parse_datetime_str(s):
    try:
        dt = datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        dt = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    return dt

