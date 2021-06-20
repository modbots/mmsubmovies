import re
import asyncio
import math
import os
import time
import requests
import urllib.request
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from bot.config import config
from random import randint
from pyrogram import filters
from time import sleep
from bot.helpers.sql_helper import gDriveDB


class CustomFilters:
    auth_users = filters.create(lambda _, __, message: bool(gDriveDB.search(message.from_user.id)))


def humanbytes(size: int) -> str:
    if not size:
        return ""
    power = 2 ** 10
    number = 0
    dict_power_n = {
        0: " ",
        1: "K",
        2: "M",
        3: "G",
        4: "T",
        5: "P"
    }
    while size > power:
        size /= power
        number += 1
    return str(round(size, 2)) + " " + dict_power_n[number] + 'B'

    # (c) @AbirHasan2005


async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n".format(
            ''.join(["●" for i in range(math.floor(percentage / 5))]),
            ''.join(["○" for i in range(20 - math.floor(percentage / 5))])
            )

        tmp = progress + config.PROGRESS.format(
            round(percentage, 2),
            humanbytesz(current),
            humanbytesz(total),
            humanbytesz(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="**{}**\n\n {}".format(
                    ud_type,
                    tmp
                ),
                parse_mode='markdown'
            )
        except:
            pass


def humanbytesz(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

async def javfetch(url):
    newUrl = url

    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'whateveyuyr')
    filename = "r.html"
    try:
        r = opener.retrieve(newUrl, filename)
    except HTTPError:
        Error = "Cannot Download"
        return Error
    await asyncio.sleep(5)
    #r = requests.get(newUrl, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"})
    url = "r.html"
    page = open(url, encoding="utf8")
    soupss = BeautifulSoup(page.read(), "html.parser")

       
#    soupss = BeautifulSoup(html, "html.parser")
    for iframe in soupss:
        iframe = soupss.find("iframe")
        aaa = iframe.get('src')
        titles = str(soupss.find('title')).replace('<title>', '').replace('</title>', '').replace('JAVCHILL', 'MMSUB.CO')
        if aaa is not None:
            return aaa, titles
        else:
            aaa = 'noon'
            return aaa, titles
