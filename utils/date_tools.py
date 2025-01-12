# -*- coding: UTF-8 -*-
# @author: ylw
# @file: DateTools
# @time: 20243/10/01
# @desc:
import re
import time
import pandas as pd
from datetime import datetime, timedelta
from datetime import date as datetime_date
from typing import List, Tuple, Union, Optional
from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta


def get_oneday_seconds() -> int:
    """
    获得一天的秒数
    """
    return 60 * 60 * 24


def get_now_timestamp(unit='ms', as_int=False) -> Union[str, int]:
    rate = 1000 if unit == 'ms' else 1
    ts = int(time.time() * rate)
    if as_int:
        return ts
    return str(ts)


def get_now_time(mode='%Y-%m-%d %H:%M:%S') -> str:
    return datetime.now().strftime(mode)


def get_now_timestamp13(as_int=False) -> Union[str, int]:
    t = int(time.time() * 1000)
    if as_int:
        return t
    return str(t)


def timestr_to_timestamp(str_time: str, mode="%Y-%m-%d %H:%M:%S") -> int:
    try:
        timeArray = time.strptime(str_time, mode)
    except ValueError as e:
        timeArray = time.strptime(str_time, "%Y-%m-%d")
    # 转换成时间戳
    return int(time.mktime(timeArray))


def timestamp_to_timestr(time_stamp: Union[str, int], mode="%Y-%m-%d %H:%M:%S") -> str:
    """
    仅支持10位时间戳
    """
    if isinstance(time_stamp, int):
        time_stamp = str(time_stamp)
    if len(time_stamp) >= 10:
        time_stamp = time_stamp[:10]
    return str(time.strftime(mode, time.localtime(int(time_stamp))))


def time_expr2s(time_str: str, time_format: Optional[str] = None) -> int:
    """
    时间表达式转为秒
    :param time_str: 01:16
    :param time_format: "%H:%M:%S"
    :return: int
    """
    if not time_str:
        return 0
    time_str = str(time_str)
    symbol_map = {1: "%M:%S", 2: "%H:%M:%S"}
    time_format = symbol_map.get(time_str.count(":"), "%H:%M:%S") if time_format is None else time_format

    # 解析时间字符串为 datetime 对象，基准日期为任意日期，这里选择同一天
    time_obj = datetime.strptime(time_str, time_format)
    # 计算秒数
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second


def time_text2s(time_text: str) -> int:
    """
    时间文本转为秒 1分16秒
    :param time_text:
    :return:
    """
    pattern = re.compile(r'(?:(\d+)年)?(?:(\d+)月)?(?:(\d+)周)?(?:(\d+)天)?(?:(\d+)(?:时|小时))?(?:(\d+)分)?(?:(\d+)秒)?')
    match = pattern.match(time_text)

    if not match:
        raise ValueError("时间文本格式不正确")

    # 提取时间各部分，并将其转为秒
    years = int(match.group(1) or 0)
    months = int(match.group(2) or 0)
    weeks = int(match.group(3) or 0)
    days = int(match.group(4) or 0)
    hours = int(match.group(5) or 0)
    minutes = int(match.group(6) or 0)
    seconds = int(match.group(7) or 0)

    # 计算总秒数
    total_seconds = (
            years * 365 * 24 * 60 * 60 +
            months * 30 * 24 * 60 * 60 +
            weeks * 7 * 24 * 60 * 60 +
            days * 24 * 60 * 60 +
            hours * 60 * 60 +
            minutes * 60 +
            seconds
    )

    return total_seconds


def get_today(mode='%Y-%m-%d') -> str:
    return datetime.now().strftime(mode)


def get_now_hour() -> int:
    return datetime.now().hour


def get_yesterday(mode="%Y-%m-%d") -> str:
    yesterday = (datetime_date.today() + timedelta(-1)).strftime(mode)
    return str(yesterday)


def get_year_first_day(mode="%Y-%m-%d") -> str:
    """
    今年第一天
    """
    return str(datetime(datetime.now().year, 1, 1).strftime(mode))


def get_last_year() -> int:
    """
    获得去年 年份
    """
    current_year = datetime.now().year
    return current_year - 1


def get_monday_date(beginDate: str, endDate: str) -> List[str]:
    """
    获得时间区间内的所有 周一的日期
    """
    start_date = datetime.strptime(beginDate, "%Y-%m-%d")
    end_date = datetime.strptime(endDate, "%Y-%m-%d")

    # 确保 start_date 是周一
    while start_date.weekday() != 0:
        start_date += timedelta(days=1)

    mondays = []
    current_date = start_date
    while current_date <= end_date:
        mondays.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(weeks=1)
    return mondays


def get_current_monday_date(base_time: str = None, *, mode="%Y-%m-%d") -> str:
    """
    获取本周周一的日期
    """
    base_time = base_time or get_today(mode)
    if isinstance(base_time, str):
        base_time = datetime.strptime(base_time, mode)

    offset = (base_time.weekday() - 0) % 7
    last_monday = base_time - timedelta(days=offset)
    return last_monday.date().strftime(mode)


def get_last_week_start_and_end(base_time=None, *, mode="%Y-%m-%d") -> Tuple[str, str]:
    """
    获取上个周一的开始和结束日期
    """
    current_monday_str = get_current_monday_date(base_time, mode=mode)
    last_week_start = day_sub(current_monday_str, offset=7, mode=mode)
    last_week_end = day_sub(current_monday_str, offset=1)
    return last_week_start, last_week_end


def get_last_monday_date(base_time=None, *, mode="%Y-%m-%d") -> str:
    """
    获取上周一的日期
    """
    return get_last_week_start_and_end(base_time, mode=mode)[0]


def get_recent_weeks_start_and_end(n: int, *, base_time=None, reverse: bool = True) -> List[tuple]:
    """
    获取从上周开始 最近 n 周的开始和结束日期
    :param n: 需要获取的周数
    :param base_time: 基准时间，如果为 None，则默认为当前时间
    :param reverse: 排序 默认倒叙
    :return: 最近 n 周的开始和结束日期列表
    """
    weeks = []
    current_week_start = get_last_monday_date(base_time)

    for _ in range(n):
        week_end = day_sub(current_week_start, offset=-6)
        weeks.append((current_week_start, week_end))
        current_week_start = day_sub(current_week_start, offset=7)

    if reverse:
        return weeks
    return weeks[::-1]


def get_current_first_day_of_month(base_time: str = None, *, mode="%Y-%m-%d", as_str=True) -> Union[str, datetime]:
    """
    获得本月第一天
    """
    if base_time is None:
        base_time = datetime.today()
    elif isinstance(base_time, str):
        base_time = datetime.strptime(base_time, "%Y-%m-%d")
    else:
        raise TypeError('base_time 参数类型不匹配')

    current_first_day_of_month = base_time.replace(day=1)
    if as_str:
        return current_first_day_of_month.strftime(mode)
    return current_first_day_of_month


def last_month_start_and_end(base_time: str = None, *, mode: str = "%Y-%m-%d") -> Tuple[str, str]:
    """
    获取上月第一天和最后一天
    """
    if base_time is None:
        base_time = datetime.today()
    elif isinstance(base_time, str):
        base_time = datetime.strptime(base_time, "%Y-%m-%d")
    else:
        raise TypeError('base_time 参数类型不匹配')

    last_day_of_last_month = datetime_date(base_time.year, base_time.month, 1) - timedelta(1)
    first_day_of_last_month = datetime_date(last_day_of_last_month.year, last_day_of_last_month.month, 1)

    return first_day_of_last_month.strftime(mode), last_day_of_last_month.strftime(mode)


def get_first_day_of_last_month(base_time: str = None, *, mode: str = "%Y-%m-%d") -> str:
    """
    获取上月第一天
    """
    return last_month_start_and_end(base_time, mode=mode)[0]


def auto_format_str_time(str_date, mode="%Y-%m-%d", safe=False):
    """
    自动识别字符串时间, 并格式化为 目标格式, 会有误差
    """
    if safe and not str_date:
        return str_date
    date_obj = dateutil_parser.parse(str_date)
    formatted_date = date_obj.strftime(mode)
    return formatted_date


def manually_format_str_time(str_time: str, *, current_mode, mode='%Y-%m-%d %H:%M:%S') -> str:
    """
    手动识别字符串时间, 并格式化为 目标格式
    """
    if not isinstance(str_time, str):
        str_time = str(str_time)

    date = datetime.strptime(str_time, current_mode).strftime(mode)
    return date


def split_date_range(begin, end, *, dt='d', mode="%Y-%m-%d", split_d: int = 1, reverse: bool = False) -> List[str]:
    """
    把目标时间区间 分割为目标格式
    """
    if dt == 'm':
        results = [pd.Timestamp(x).strftime(mode) for x in pd.date_range(begin, end, freq='MS')]
    elif dt == 'd':
        results = [x.strftime(mode) for x in list(pd.date_range(start=begin, end=end))]
    else:
        results = []

    if reverse is True:
        results = results[::-1]
    if split_d > 1:
        l_result = len(results)
        results = [results[index] for index in range(0, l_result, split_d)]

    return results


def sort_dates(date_list: list, *, date_format="%Y-%m-%d", reverse=False) -> list:
    """
    对包含日期字符串（格式为 "%Y-%m-%d"）的列表进行排序。
    :param date_list: 包含日期字符串的列表，例如 ["2024-08-22", "2023-12-01", "2024-01-15"]
    :param date_format: 格式化格式
    :param reverse: 默认升序, False:升序, True: 降序
    :return: 排序后的日期字符串列表(正序)
    """
    return sorted(date_list, key=lambda date_str: datetime.strptime(date_str, date_format), reverse=reverse)


def days_difference(t1: str, t2: str) -> int:
    """
    获得两个时间的差值 mode="%Y-%m-%d"
    """
    t1_t = datetime.strptime(t1, "%Y-%m-%d")
    t2_t = datetime.strptime(t2, "%Y-%m-%d")
    difference = int((t2_t - t1_t).total_seconds() / (24 * 3600))
    return difference


def day_sub(base_t: str, offset: int, mode="%Y-%m-%d") -> str:
    """
    base_t 偏移 offset 天之后的日期
    """
    if not isinstance(base_t, str):
        base_t = str(base_t)
    return (datetime.strptime(base_t, mode) - relativedelta(days=offset)).strftime(mode)


def add_seconds(base_t: str = None, seconds: int = 0, mode="%Y-%m-%d %H:%M:%S") -> str:
    """
    seconds 偏移 offset 秒之后的时间
    """
    if base_t is None:
        base_t = get_now_time(mode=mode)
    return (datetime.strptime(base_t, mode) + timedelta(seconds=seconds)).strftime(mode)


def year_calculation(target_str: str, today: str = get_today()) -> str:
    """
    用来计算丢失的年份
    :param target_str: %m-%d
    :param today: "%Y-%m-%d"
    :return:
    """
    now_time_t = datetime.strptime(today, "%Y-%m-%d")

    # 这里给它一个假的年份
    target_t = datetime.strptime(f"{now_time_t.year}-{target_str}", "%Y-%m-%d")

    if target_t.month > now_time_t.month:
        year = str(get_last_year())
    else:
        year = get_year_first_day("%Y")
    return f"{year}-{target_str}"


def group_dates(date_list: List[str], mode="%Y-%m-%d", split_day=0) -> List[Tuple[str, str]]:
    """
    将日期按连续性分组，并且每组的日期范围超过 split_day 天进行分割。
    """
    date_list = list(set(date_list))
    if not date_list:
        return []

    date_objects = [datetime.strptime(date, mode) for date in date_list]
    date_objects.sort()  # 排序日期
    grouped_dates = []  # 用于存储结果

    start_date = date_objects[0]
    end_date = start_date

    def add_group(start, end):
        if split_day <= 1:
            grouped_dates.append((start_date.strftime(mode), end_date.strftime(mode)))
            return
        while start <= end:
            split_end = min(start + timedelta(days=split_day), end)
            grouped_dates.append((start.strftime(mode), split_end.strftime(mode)))
            start = split_end + timedelta(days=1)

    for index in range(1, len(date_objects)):
        if date_objects[index] == end_date + timedelta(days=1):
            end_date = date_objects[index]
            continue

        add_group(start_date, end_date)
        start_date = date_objects[index]
        end_date = start_date

    # 添加最后一组
    add_group(start_date, end_date)
    return grouped_dates


# def utc_time_to_standard_time(utc_time: str):
#     """
#     将格林尼治时间 转为 标准得东八区时间
#     :param utc_time: '2022-11-03T02:44:48.000+0000'
#     :return:东八区时间
#     """
#     t = utc_time[:-9]
#     utc_date2 = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S")
#     local_date = utc_date2 + datetime.timedelta(hours=8)
#     return datetime.datetime.strftime(local_date, "%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    print(timestamp_to_timestr(1730786470))
    print(last_month_start_and_end())
    # print(day_sub(get_today(), 2))
    # print(get_now_time('%Y%m%d_%H%M%S'))
    # print(time_text2s('1天16秒'))
    # print(get_now_timestamp(as_int=True))
    # print(get_current_monday_date())
    # print(last_month_start_and_end('2024-01-15'))
    # aa, cc = get_last_week_start_and_end()
    # print(aa, cc)
    # print(get_current_monday_date())
    #
    # print(get_recent_weeks_start_and_end(12, reverse=False))
    #
    # start_time = day_sub(get_yesterday(), 2, '%Y-%m-%d')
    # end_time = get_yesterday('%Y-%m-%d')
    #
    # get_date_list = split_date_range(start_time, end_time)[::-1]
    print((timestr_to_timestamp('2024-10-08')))

    print(time_expr2s('01:45'))
    print( day_sub(get_today(), 2))
    # print(sort_dates(['2024-08-11', '2024-08-13', '2024-08-12'], reverse=True))
