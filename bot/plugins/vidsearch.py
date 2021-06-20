#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from pickle import TRUE
logger = logging.getLogger(__name__)
import wget
import os
import random
import requests
import json
import glob
import urllib
import time
import aiohttp
import urllib.request
from urllib.parse import urlparse
from urllib.error import HTTPError
from pyrogram import Client, filters
from bot.config import BotCommands, Messages
from bot.helpers.utils import CustomFilters
from bot.helpers.screenshots import generate_screen_shots
from bot import LOGGER, DOWNLOAD_DIRECTORY
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Message
from bot.helpers.sql_helper import urlbyMsg
from bot.helpers.screenshots import generate_thumb
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from bot.helpers.uploader import send_video_handler, send_video_channel
from bot.helpers.utils import CustomFilters, humanbytes, TimeFormatter
from bot.helpers.sql_helper import urldb

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Vidsearch) & CustomFilters.auth_users)

async def mmsub(bot, message):
    user_id = message.from_user.id
    search = message.text.split(' ',maxsplit=1)[1]
#    sent_message = await message.reply_text('🕵️**Searching Video link...**', quote=True)
#    LOGGER.info(f'VIDSEARCH:{user_id}: {search}')
    getApi = "https://raw.githubusercontent.com/modbots/backen/main/api.txt"  
    dl_path = DOWNLOAD_DIRECTORY
    try:
      filename = wget.download(getApi, dl_path)
    except HTTPError:
        upgrade = "Please Upgrade because Our Free Api Load Too Much"
        await message.reply_text(upgrade)
    app = open(dl_path + "/" + "api.txt", 'r')
    for api in app:
        api = api.strip()
    api = requests.get(api + str(search))
    data = api.json()
    if data == []:
        await message.reply_text("No such movies here")
    else:
        with open('data.json', 'w') as f:
            json.dump(data, f)
        with open('data.json') as json_file:
            datas = json.load(json_file)
            for p in datas:
                names =  p['link']
                size = p['size_gb']
        msg_id = message.message_id
        cb_msg_id = int(msg_id + 1)
        urlbyMsg._set(cb_msg_id, names)
        parasename = urlparse(names)
        basename = os.path.basename(parasename.path)
        name = basename.replace("%20", " ")
        await message.reply_text(
                            text="ကျွန်တော် တို့ဆာဗာတွင် " + str(name) + " ဟုဆိုသော ဇတ်ကားတစ်ကား တွေ့ရှိပါသည်။၄င်းဖိုင်သည် " + str(size) + " GB ခန့်ရှိသည်။ ",
                            parse_mode="Markdown",
                            reply_markup=InlineKeyboardMarkup([
                                                                [InlineKeyboardButton("‌ဒေါင်းလုပ်ဆွဲမည်", callback_data="download"),
                                                                InlineKeyboardButton("မဆွဲတော့ပါ", callback_data="notnow")]
                                                                ]),
                            disable_web_page_preview=True
                        )

@Client.on_callback_query()
async def button(bot, message: CallbackQuery):
    cb_data = message.data  
    user_id = message.from_user.id
    dl_ = 'downloads/' + str(user_id)
    if not os.path.exists(dl_):
        os.makedirs(dl_)
    if "download" in cb_data:
        cb_msg_id = message.message.message_id
        cb_url = urlbyMsg.search_url(cb_msg_id)
               
#        cb_url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4"
#       LOGGER.info(f'DOWNLOADING:{user_id}: {cb_url}')
        LOGGER.info(f'Checking Size: {cb_url}')
        response = requests.head(cb_url)
        before = response.headers.get("Content-Length")
        if (int(before) > 2097152000):
            await bot.send_message(
					chat_id=message.message.chat.id,
					text="၄င်းဖိုင်သည် 2GB ကျော်လွန်နေပါသဖြင့် TELEGRAM သို့တင်လို့မရပါ"
				)
        else:
            dl_path = './downloads/' + str(user_id)
            if not os.path.exists(dl_path):
                os.makedirs(dl_path)
            parasenames = urlparse(cb_url)
            basename = os.path.basename(parasenames.path)
            names = basename.replace("%20", " ")
            filename = os.path.join(dl_path, names)
#            opener = urllib.request.URLopener()
#            opener.addheader('User-Agent', 'whateveyuyr')
#            start = await bot.send_message(
#                    chat_id=message.message.chat.id,
#                    text="စတင်ဒေါင်းလုပ်ဆွဲနေပါပြီ...",
#               )
            locdl = str(user_id)
            LOGGER.info(f'DOWNLOADING:{user_id}: {cb_url}')
            #dl_url = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
            async with aiohttp.ClientSession() as session:
                c_time = time.time()
              
                await download_coroutine(
                        bot,
                        session,
                        cb_url,
                        filename ,
                        message.message.chat.id,
                        message.message.message_id,
                        c_time
                    )
               
                #return False
            if not os.path.exists("crd.txt"):
                wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
            pb = open("pb.txt", 'r')
            for l in pb:
                l = l.strip()
            await bot.send_message(
                        chat_id=message.message.chat.id,
                        text="Generating Screenshots..."
                    )
            images = await generate_screen_shots(
                                    filename,
                                    dl_path,
                                    False,
                                    Messages.START,
                                    5,
                                    9,
                                    locdl
                                )	
            logger.info(images)
            screenshots = []
            if images is not None:
                i = 0
                caption = str(names).replace('.mp4',' ').replace('.mkv',' ') + l
                for image in images:
                    if os.path.exists(image):
                        if i == 0:
                            screenshots.append(
                                InputMediaPhoto(
                                    media=image,
                                    caption=caption,
                                    parse_mode="html"
                                    )
                                )
                        else:
                            screenshots.append(
                                InputMediaPhoto(
                                    media=image
                                    )
                                )
                        i = i + 1

            editable = await bot.send_message(
                                                    chat_id=message.message.chat.id,
                                                    text= "wait for a moment",
                    
                                )
            output_vid = dl_path + '/' + names
            width = 100
            height = 100
            duration = 0
            metadata = extractMetadata(createParser(output_vid))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")	
            thumbdir = DOWNLOAD_DIRECTORY + str(message.from_user.id) + "/"
            if not os.path.isdir(thumbdir):
                os.makedirs(thumbdir)
            video_thumbnails = thumbdir + names + ".jpg"
            if not os.path.exists(video_thumbnails):
                video_thumbnail = await generate_thumb(
                                    output_vid,
                                    os.path.dirname(thumbdir),
                                    names,
                                    random.randint(
                                        0,
                                        duration - 1
                                        )
                                    )
            
            file_size = os.path.getsize(output_vid)
            if (int(file_size) > 2097152000):
                await bot.send_message(
                                                    chat_id=message.message.chat.id,
                                                    text= "We Cannot upload",
                                        )
            isd = message.message
            sent_vid = await send_video_handler(bot, isd, output_vid, video_thumbnails, duration, width, height, editable, file_size)
            await editable.delete()
            os.remove(video_thumbnails)
            filelist = glob.glob(os.path.join(dl_path, "*.*"))
            for f in filelist:
                os.remove(f) 

async def check_vid(movies):
    search = movies
#    sent_message = await message.reply_text('🕵️**Searching Video link...**', quote=True)
#    LOGGER.info(f'VIDSEARCH:{user_id}: {search}')
    getApi = "https://raw.githubusercontent.com/modbots/backen/main/api.txt"  
    dl_path = DOWNLOAD_DIRECTORY
    try:
      filename = wget.download(getApi, dl_path)
    except HTTPError:
        upgrade = "upgrade"
        return upgrade
    app = open(dl_path + "/" + "api.txt", 'r')
    for api in app:
        api = api.strip()
    api = requests.get(api + str(search))
    data = api.json()
    if data == []:    
        return data
    else:
        with open('data.json', 'w') as f:
            json.dump(data, f)
        with open('data.json') as json_file:
            datas = json.load(json_file)
            for p in datas:
                names =  p['link']
                size = p['size_gb']
        cb_url = names
    return cb_url


async def download_vid(bot,message, movies, location):
    search = movies
    locdl = location
#    sent_message = await message.reply_text('🕵️**Searching Video link...**', quote=True)
#    LOGGER.info(f'VIDSEARCH:{user_id}: {search}')
    getApi = "https://raw.githubusercontent.com/modbots/backen/main/api.txt"  
    dl_path = DOWNLOAD_DIRECTORY
    try:
      filename = wget.download(getApi, dl_path)
    except HTTPError:
        upgrade = "Please Upgrade Plan"
        return upgrade
    app = open(dl_path + "/" + "api.txt", 'r')
    for api in app:
        api = api.strip()
    api = requests.get(api + str(search))
    data = api.json()
    if data == []:
        upgrade = "No Such Movies Here"
        return upgrade
    else:
        with open('data.json', 'w') as f:
            json.dump(data, f)
        with open('data.json') as json_file:
            datas = json.load(json_file)
            for p in datas:
                names =  p['link']
                size = p['size_gb']
        cb_url = names
        #cb_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" 
        predownload =  await bot.send_message(
                        chat_id=message.message.chat.id,
                        text="ပြင်ဆင်နေပြီ" 
                    )       

        dl_pathr = DOWNLOAD_DIRECTORY + locdl
        if not os.path.exists(dl_pathr):
                os.makedirs(dl_pathr)
        parasenames = urlparse(cb_url)
        basename = os.path.basename(parasenames.path)
        names = basename.replace("%20", " ")
        filename = os.path.join(dl_pathr, names)
        async with aiohttp.ClientSession() as session:
                c_time = time.time()      
              
                downloading = await download_coroutine(
                        bot,
                        session,
                        cb_url,
                        filename ,
                        message.message.chat.id,
                        predownload.message_id,
                        c_time
                    )
        if not os.path.exists("crd.txt"):
            wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
        pb = open("pb.txt", 'r')
        for l in pb:
            l = l.strip()
        await predownload.delete()
        await bot.send_message(
                        chat_id=message.message.chat.id,
                        text="သင်တောင်းဆိုတဲ့ " + str(names) + " ကို ဒေါင်းပြီးပါပြီ "
                    )       
        ssgen = await bot.send_message(
                        chat_id=message.message.chat.id,
                        text="Generating Screenshots..." + str(names)
                    )       
        images = await generate_screen_shots(
								filename,
								dl_pathr,
								False,
								Messages.START,
								5,
								9,
                                locdl
							)	
      
        files = []
        if images is not None:
            i = 0
            caption = l
            for image in images:
                if os.path.exists(image):
                    if i == 0:
                        files.append(
                            InputMediaPhoto(
                                media=image,
                                caption=caption,
                                parse_mode="html"
                                )
                            )
                    else:
                        files.append(
                            InputMediaPhoto(
                                media=image
                                )
                            )
                    i = i + 1
        chid = urldb.search_url(message.from_user.id)
        await bot.send_media_group(
                            chat_id=chid,
                            disable_notification=True,
                            media=files
                            )
        await ssgen.edit("SCREENSHOTS များလွှင့်တင်ပြီးပါပြီ")
        
        editable = await bot.send_message(
                                                    chat_id=message.message.chat.id,
                                                    text= "wait for uploading",
                    
                                )
        output_vid = dl_pathr + '/' + names
        width = 100
        height = 100
        duration = 0
        metadata = extractMetadata(createParser(output_vid))
        if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        if metadata.has("width"):
                width = metadata.get("width")
        if metadata.has("height"):
                height = metadata.get("height")	
        thumbdir = DOWNLOAD_DIRECTORY + str(message.from_user.id) + "/"
        if not os.path.isdir(thumbdir):
                os.makedirs(thumbdir)
        video_thumbnails = thumbdir + names + ".jpg"
        if not os.path.exists(video_thumbnails):
                video_thumbnail = await generate_thumb(
                                    output_vid,
                                    os.path.dirname(thumbdir),
                                    names,
                                    random.randint(
                                        0,
                                        duration - 1
                                        )
                                    )
            
        file_size = os.path.getsize(output_vid)
        if (int(file_size) > 2097152000):
                await bot.send_message(
                                                    chat_id=message.message.chat.id,
                                                    text= "We Cannot upload",
                                        )
        
        sent_vid = await send_video_channel(bot, chid, output_vid, video_thumbnails, duration, width, height, editable, file_size, names)
        await editable.delete()
        await bot.send_message(
                                                    chat_id=message.message.chat.id,
                                                    text= "သင့်ချန်နယ်‌ပေါ် တင်ပြီးပါပြီ ",
                    
                                )
        os.remove(video_thumbnails)
        os.remove(output_vid)
        filelist = glob.glob(os.path.join(dl_path, "*.png"))
        for f in filelist:
            os.remove(f) 

async def outputr(movies):
    search = movies
#    sent_message = await message.reply_text('🕵️**Searching Video link...**', quote=True)
    LOGGER.info(f'CNFVIDSEARCH: {search}')
    getApi = "https://raw.githubusercontent.com/modbots/backen/main/api.txt"  
    dl_path = DOWNLOAD_DIRECTORY
    try:
      filename = wget.download(getApi, dl_path)
    except HTTPError:
        upgrade = "Please Upgrade Plan"
        return upgrade
    app = open(dl_path + "/" + "api.txt", 'r')
    for api in app:
        api = api.strip()
    api = requests.get(api + str(search))
    data = api.json()
    if data == []:
        upgrade = "No Such Movies Here"
        return upgrade
    else:
        with open('data.json', 'w') as f:
            json.dump(data, f)
        with open('data.json') as json_file:
            datas = json.load(json_file)
            for p in datas:
                names =  p['link']
                size = p['size_gb']
        cb_url = names
 #       cb_url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4"
#       LOGGER.info(f'DOWNLOADING:{user_id}: {cb_url}')
        dl_path = DOWNLOAD_DIRECTORY  
        parasenames = urlparse(cb_url)
        basename = os.path.basename(parasenames.path)
       

        return basename

async def before(movies):    
    cb_url = movies
    response = requests.head(cb_url)
    before = response.headers.get("Content-Length")
    if (int(before) > 2097152000):
        ok = "false"
        return ok
    else:
        ok = "true"
        return ok

async def download_coroutine(bot, session, url, file_name, chat_id, message_id, start):
    downloaded = 0
    PROCESS_MAX_TIMEOUT = 0
    CHUNK_SIZE = 128
    display_message = ""
    async with session.get(url, timeout=PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])        
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        parasename = urlparse(url)
        basename = os.path.basename(parasename.path)
        name = basename.replace("%20", " ")
        fakeurl = "https://mmsub.co/" + name
        fakeserver = "mmsub.co"
        await bot.edit_message_text(
            chat_id,
            message_id,
            text="""Initiating Download
SERVER: {}
File Size: {}""".format(fakeserver, humanbytes(total_length))
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """**Download Status**
URL: {}
File Size: {}
Downloaded: {}
Speed {}/s
ETA: {}""".format(
    fakeurl,
    humanbytes(total_length),
    humanbytes(downloaded),
    humanbytes(speed),
    TimeFormatter(estimated_total_time)
)
                        if current_message != display_message:
                            await bot.edit_message_text(
                                chat_id,
                                message_id,
                                text=current_message
                            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()
