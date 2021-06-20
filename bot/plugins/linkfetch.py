import requests 
import bs4
import os 
import glob
import random
import aiohttp
import time
import asyncio
import aiohttp
import wget
from urllib.parse import urlparse
from bot.helpers.screenshots import generate_thumb
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from bot.helpers.uploader import send_video_handler, send_video_channel
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Message
from bot.config import BotCommands, Messages
from bot import LOGGER, DOWNLOAD_DIRECTORY
from bot.plugins.vidsearch import check_vid, download_vid, outputr, before, download_coroutine
from bot.plugins.cmdescription import cmlinkfetch
from bot.helpers.screenshots import generate_screen_shots
from bot.helpers.sql_helper import urldb

@Client.on_message(filters.private & filters.incoming & filters.command(['fetch']))

async def linkfetch(client, message):
    user_id = message.from_user.id
    chid = urldb.search_url(user_id)
    if chid == "NOON":
        await message.reply_text(
            text="ခင်ဗျား ချန်နယ် ကို အရင် ပြော ထား ဗျ ... လခွမ်း ပဲ"    
            )
    else:
        LOGGER.info(f'DOWNLOADING: walking')
        links = open(str(user_id) + ".txt", 'r')
        for link in links:
            await client.send_message(chat_id = message.chat.id,
                            text = "ယခုလွှင့်တင်မည့် လင့် \n" + link)
            await load_url(link, client, message)
            

async def load_url(url, client, message):          
            request_result = requests.get( url )
            soup = bs4.BeautifulSoup( request_result.text 
                                    , "html.parser" )
            mydivs = soup.find_all("div", {"class": "data"})
            for name in mydivs:
                name = name.findAll('h1')
                movies = str(name).replace('[<h1 itemprop="name">', '').replace('</h1>]', '')
                LOGGER.info(f'Checking: {movies}')
                data = await check_vid(movies)
                if data == []:
                    noon = "no such movies " + movies + " on our server. "
                    await client.send_message(chat_id = message.chat.id,
                    text = noon)
                else:
                    LOGGER.info(f'Checking Size: {movies}')
                    ok = await before(data)
                    okk = str(ok)
                    fz = "false"
                    if okk == fz:
                        await client.send_message(chat_id = message.chat.id,
                        text = "၄င်း " + movies + " သည် 2GB ကျော်လွန်နေပါသဖြင့် TELEGRAM ပေါ်သို့တင်လို့မရပါ")
                    else:
                        
                        await download(client, message, data, movies)


async def download(client, message, data, movies):
    async with aiohttp.ClientSession() as session:
        output = DOWNLOAD_DIRECTORY + str(message.from_user.id) + "/"
        location = str(message.from_user.id)
        chid = urldb.search_url(location)
        if not os.path.isdir(output):
            os.makedirs(output)
        LOGGER.info(f'DOWNLOADING: {movies}')
                            #files = await download_vid(movies, location)
        a = await client.send_message(chat_id = message.chat.id,
                                text = "၄င်း " + movies + " ဆိုတဲ့ ကားကို ဒေါင်းနေပါပြီဗျာ...")
        dl_path = DOWNLOAD_DIRECTORY + location
        parasenames = urlparse(data)
        basename = os.path.basename(parasenames.path)
        names = basename.replace("%20", " ")
        filename = os.path.join(dl_path, names)   
        c_time = time.time()
        
        datas = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"                       
        files = await download_coroutine(
                client,
                session,
                datas,
                filename ,
                a.chat.id,
                a.message_id,
                c_time
                )

        images = await generate_screen_shots(
								filename,
								dl_path,
								False,
								Messages.START,
								5,
								9,
                                location
							)	
      
        screenshots = []
        if images is not None:
            i = 0
            caption = str(names).replace('.mp4',' ').replace('.mkv',' ') + " powered by mmsub.co"
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
        
                
        await client.send_media_group(
                                        chat_id=chid,
                                        disable_notification=True,
                                        media=screenshots
                                        )
        cm_desp = cmlinkfetch(movies)
        await client.send_message(chat_id = message.chat.id,
                            text = cm_desp)
        
        output_vid = filename
                                
        editable = await client.send_message(
                                                    chat_id=message.chat.id,
                                                    text= "လွှင့်တင်ဖို့ ပြင်ဆင်နေပြီကွာ....",
                                        )
        if os.path.exists(output_vid):
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
            if not os.path.exists(video_thumbnails):
                thumburl = "https://raw.githubusercontent.com/modbots/backen/main/default.jpg"
                wget.download(thumburl, dl_path)
                video_thumbnails = dl_path + "/default.jpg"
                #sent_vid = await send_video_handler(client, message, output_vid, video_thumbnails, duration, width, height, editable, file_size)
                sent_vid = await send_video_channel(client, chid, output_vid, video_thumbnails, duration, width, height, editable, file_size, names)
            else:
                sent_vid = await send_video_channel(client, chid, output_vid, video_thumbnails, duration, width, height, editable, file_size, names)
                os.remove(video_thumbnails)
            await editable.delete() 
            await a.delete()          
            filelist = glob.glob(os.path.join(output, "*.png"))
            for f in filelist:
                os.remove(f)
        else:
            await a.delete() 
            await editable.delete()
            await client.send_message(
                                                        chat_id=message.chat.id,
                                                        text= "တခုခုတော့ လွဲနေပြီ မင်း မိုးဒီယူ ကို အ‌‌‌ကြောင်းကြားလိုက်ပါ",
                                            )
