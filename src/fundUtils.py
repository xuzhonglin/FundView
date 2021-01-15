import datetime
from chinese_calendar import get_workdays

from typing import List


def _correct_trading_day(trading_day: List[datetime.date], last_work_day: datetime.date):
    trading_day_date = trading_day[0]
    trading_day_length = len(trading_day)
    if trading_day[0].day != last_work_day.day:
        for i in range(1, len(trading_day)):
            if trading_day[i].day == last_work_day.day:
                trading_day_date = trading_day[i]
                trading_day_length = len(trading_day) - i
                break
    return trading_day_date, trading_day_length


def get_last_trading_day(type: str):
    """
    获取上一个交易日
    :return: 日期
    """
    today = datetime.date.today()
    last_day = today - datetime.timedelta(days=1)
    last_month = today - datetime.timedelta(days=31)

    last_work_day = get_workdays(last_month, last_day)[-1]
    trading_day_date = last_day
    trading_day_length = 0
    if type == 'ONE_MONTH':
        last_month = last_work_day - datetime.timedelta(days=31)
        trading_day = get_workdays(last_month, last_work_day)
        trading_day_date, trading_day_length = _correct_trading_day(trading_day, last_work_day)
    elif type == 'THREE_MONTH':
        last_three_month = last_work_day - datetime.timedelta(days=31 * 3)
        trading_day = get_workdays(last_three_month, last_work_day)
        trading_day_date, trading_day_length = _correct_trading_day(trading_day, last_work_day)

    elif type == 'SIX_MONTH':
        last_six_month = last_work_day - datetime.timedelta(days=31 * 6)
        trading_day = get_workdays(last_six_month, last_work_day)
        trading_day_date, trading_day_length = _correct_trading_day(trading_day, last_work_day)

    elif type == 'ONE_YEAR':
        last_year = last_work_day - datetime.timedelta(days=366)
        trading_day = get_workdays(last_year, last_work_day)
        trading_day_date, trading_day_length = _correct_trading_day(trading_day, last_work_day)

    elif type == 'THREE_YEAR':
        last_three_year = last_work_day - datetime.timedelta(days=366 * 3)
        trading_day = get_workdays(last_three_year, last_work_day)
        trading_day_date, trading_day_length = _correct_trading_day(trading_day, last_work_day)

    return trading_day_date.strftime('%Y-%m-%d'), trading_day_length


def judge_time(target_time: str):
    nowTime = datetime.datetime.now()
    hour = int(target_time.split(':')[0])
    minute = int(target_time.split(':')[1])
    seconds = int(target_time.split(':')[2])
    return nowTime.hour >= hour and nowTime.minute >= minute and nowTime.second >= seconds
