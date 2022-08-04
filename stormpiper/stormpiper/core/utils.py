import asyncio
import datetime
from typing import List, Optional

import pandas
import pytz
from celery.result import AsyncResult


def columns_of_dtype(df: pandas.DataFrame, selector: str) -> List[str]:
    """get columns of df that  match the 'selector' dtype

    e.g.,
    >columns_of_dtype(df, 'datetime')
    output: ['time_created', 'time_updated']

    """
    return [c for c in df.columns if selector in str(df[c].dtype)]


def datetime_to_isoformat(df, cols=None, dt_selector=None, inplace=False):
    """create json serializable timestamps by converting all datetime columns to isoformat"""
    if dt_selector is None:
        dt_selector = "datetime"
    if cols is None:
        cols = columns_of_dtype(df, dt_selector)
    if not inplace:
        df = df.copy()

    df[cols] = df[cols].applymap(lambda x: x.isoformat())

    return df


async def wait_a_sec_and_see_if_we_can_return_some_data(
    task: AsyncResult,
    timeout: Optional[float] = None,
    exp: Optional[float] = None,
) -> None:
    if timeout is None:
        timeout = 0.5

    if exp is None:
        exp = 1

    t = 0.0
    inc = 0.05  # check back every inc seconds
    while t < timeout:
        if task.ready():  # exit even if the task failed
            return
        else:
            inc *= exp
            t += inc
            await asyncio.sleep(inc)
    return


def datetime_now():
    return datetime.datetime.now(pytz.timezone("US/Pacific"))
