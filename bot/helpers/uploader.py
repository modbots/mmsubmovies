import time
import wget
import os
from humanfriendly import format_timespan
from bot.helpers.utils import progress_for_pyrogram, humanbytesz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.helpers.sql_helper import urldb

async def send_video_channel(bot, chid, output_vid, video_thumbnail, duration, width, height, editable, file_size, names):
    c_time = time.time()
    if not os.path.exists("crd.txt"):
        wget.download('https://raw.githubusercontent.com/modbots/backen/main/crd.txt')
    app = open("crd.txt", 'r')
    for api in app:
        api = api.strip()
    if not os.path.exists("pb.txt"):
        wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
    pb = open("pb.txt", 'r')
    for l in pb:
        l = l.strip()
    name = str(names).replace("%20", " ").replace('.mp4', '').replace('.mkv', '').replace('./downloads/', '')
    sent_vid = await bot.send_video(
        chat_id=chid,
        video=output_vid,
        caption=f"**ဖိုင်နာမည် :** `{name}`\n**ကြာချိန် :** `{format_timespan(duration)}`\n**ဖိုင်ဆိုဒ် :** `{humanbytesz(file_size)}`\n\n{api} ......{l}",
        thumb=video_thumbnail,
        duration=duration,
        width=width,
        height=height,
        supports_streaming=True,
        #reply_markup=InlineKeyboardMarkup([InlineKeyboardButton("Developer", url="https://t.me/AbirHasan2005")]),
        progress=progress_for_pyrogram,
        progress_args=(
            "လွှင့်တင်နေပါပြီ ဆရာ...",
            editable,
            c_time
        )
    )
    return sent_vid
async def send_video_handler(bot, message, output_vid, video_thumbnail, duration, width, height, editable, file_size):
    c_time = time.time()
    ids = str(message.from_user.id) 
    if not os.path.exists("crd.txt"):
        wget.download('https://raw.githubusercontent.com/modbots/backen/main/crd.txt')
    app = open("crd.txt", 'r')
    for api in app:
        api = api.strip()
    if not os.path.exists("crd.txt"):
        wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
    pb = open("pb.txt", 'r')
    for l in pb:
        l = l.strip()
    name = str(output_vid).replace("%20", " ").replace('.mp4', '').replace('.mkv', '').replace('./downloads/', '').replace(ids, '')

    sent_vid = await bot.send_video(
        chat_id=message.chat.id,
        video=output_vid,
        caption=f"**ဖိုင်နာမည် :** `{name}`\n**ကြာချိန် :** `{format_timespan(duration)}`\n**ဖိုင်ဆိုဒ် :** `{humanbytesz(file_size)}`\n\n{api} ......{l}",
        thumb=video_thumbnail,
        duration=duration,
        width=width,
        height=height,
        reply_to_message_id=message.message_id,
        supports_streaming=True,
        progress=progress_for_pyrogram,
        progress_args=(
           "လွှင့်တင်နေပါပြီ ဆရာ...",
            editable,
            c_time
        )
    )
    return sent_vid

async def send_video_handler_fmax(bot, message, output_vid, video_thumbnail, duration, width, height, editable, file_size, title):
    c_time = time.time()
    ids = str(message.from_user.id) 
    if not os.path.exists("crd.txt"):
        wget.download('https://raw.githubusercontent.com/modbots/backen/main/crd.txt')
    app = open("crd.txt", 'r')
    for api in app:
        api = api.strip()
    if not os.path.exists("crd.txt"):
        wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
    pb = open("pb.txt", 'r')
    for l in pb:
        l = l.strip()
    name = str(output_vid).replace("%20", " ").replace('.mp4', '').replace('.mkv', '').replace('./downloads/', '').replace(ids, '')

    sent_vid = await bot.send_video(
        chat_id=message.chat.id,
        video=output_vid,
        caption=f"**JAV DESP:** `{title}`\n**Video Duration:** `{format_timespan(duration)}`\n**File Size:** `{humanbytesz(file_size)}`\n\n{api} ......{l} ",
        thumb=video_thumbnail,
        duration=duration,
        width=width,
        height=height,
        reply_to_message_id=message.message_id,
        supports_streaming=True,
        progress=progress_for_pyrogram,
        progress_args=(
            "လွှင့်တင်နေပါပြီ ဆရာ...",
            editable,
            c_time
        )
    )
    return sent_vid
