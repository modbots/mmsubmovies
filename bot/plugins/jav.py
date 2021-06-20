import requests
import re
import asyncio
from requests import get
import lk21
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint
import os 
import aiohttp
import time
import glob
import random
from bot.plugins.vidsearch import download_coroutine
from bot.helpers.screenshots import generate_screen_shots
from bot.helpers.downloader import download_file, download_fmax, download_poster
from bot.helpers.screenshots import generate_thumb
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from bot.helpers.uploader import send_video_handler
from pyrogram import Client, filters
from bot.config import BotCommands, Messages
from bot.helpers.utils import CustomFilters, javfetch, humanbytes
from bot import LOGGER, DOWNLOAD_DIRECTORY
from bot.plugins.vidsearch import check_vid, download_vid, outputr, before
from bot.helpers.screenshots import generate_thumb
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from bot.helpers.uploader import send_video_handler, send_video_handler_fmax, send_video_channel
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Message
from bot.helpers.sql_helper import urldb

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Javgen))
async def jav(bot, message):
    user_id = message.from_user.id
    if len(message.command) > 1:
        search = message.text.split(' ',maxsplit=1)[1]
        headers = {"Accept-Language": "en-US,en;q=0.5"}
        pages = np.arange(int(search))
        LOGGER.info(f'JAVBABES: walking')
        sent_message = await message.reply_text('🕵️**သင့်ချန်နယ်အတွက် ဂျပန်ကားများ ကိုတင်ပေးပါမည်။ တခြား ဘာမှမလုပ်ပါနဲ့ ။ ဘော့ ကို ခိုင်းတာများရင် ပျက်တတ်ပါတယ်**', quote=True)
        for page in pages: 
            page = requests.get("https://javchill.com/latestMovie/" + str(page), headers=headers)
            await asyncio.sleep(5)
            soup = BeautifulSoup(page.content, 'html.parser')   
            movie_div = soup.find_all('div', class_='Featured row')    
            for div in movie_div:
                links = div.findAll('a',onclick="pop(this)")
                for a in links:
                    newUrl = 'https://javchill.com' + a['value']
                    noon = 'https://javchill.com/play/'
                    if not newUrl == noon:
                        javurl, title = await javfetch(newUrl)
                        aaa = 'noon'
                        if not javurl == aaa:
                            if 'gasimas.xyz' in javurl:
                                dlink,plink = javurl.split("#")
                                femebed = str(dlink).replace('https://gasimas.xyz', 'https://femax20.com') 
                                poster = str(plink).replace('poster=', '')
                                dl_url = ''
                                try:
                                    link = re.findall(r'\bhttps?://.*femax20\.com\S+', femebed)[0]
                                except IndexError:
                                    print("`No Fembed links found`\n")
                                bypasser = lk21.Bypass()
                                sent_messages = await message.reply_text('🕵️**ပတ်သက်ရှာဖွေနေတယ် ခနစောင့်.. မစောင့်နိုင်ရင် လဲနေ.. **', quote=True)
                                dl_url=bypasser.bypass_fembed(link)
                                lst_link = []
                                for i in dl_url:
                                    lst_link.append(dl_url[i])
                                direct_url = lst_link[0]        
                                posterurl = poster.strip()
                                flink = direct_url.strip()
                                filename = os.path.basename(flink)
                                dl_path = DOWNLOAD_DIRECTORY + str(user_id)
                                filenames = os.path.join(dl_path, filename)   
                                if not os.path.exists(dl_path):
                                    os.makedirs(dl_path)
                                LOGGER.info(f'Download:{user_id}: {link}')
                                #await sent_message.delete()
                                bb = Messages.DOWNLOADING.format(title) 
                                cc = await sent_messages.edit(Messages.DOWNLOADING.format(title))
                                #vresult = download_fmax(flink, dl_path)
                                async with aiohttp.ClientSession() as session:
                                    c_time = time.time()
                                
                                    await download_coroutine(
                                            bot,
                                            session,
                                            flink,
                                            filenames ,
                                            user_id,
                                            sent_messages.message_id,
                                            c_time
                                        )
                                
                                presult = download_poster(posterurl, dl_path)
                                file_path = os.path.join(f"{dl_path}/{filename}")
                                
                                if os.path.exists(file_path):
                                    await cc.delete()
                                    dd = Messages.DOWNLOADED_SUCCESSFULLY.format(title, os.path.basename(file_path), humanbytes(os.path.getsize(file_path)))
                                    
                                    await bot.send_message(chat_id = message.chat.id,
                                                            text = dd,
                                                        )
                                    
                                    images = await generate_screen_shots(
                                    file_path,
                                    dl_path,
                                    False,
                                    Messages.START,
                                    5,
                                    9,
                                    str(user_id)
                                    )

                                    files = []
                                    if images is not None:
                                        i = 0
                                        caption = "© @moedyiu "
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
                                        editable = await bot.send_message(
                                                                            chat_id=message.chat.id,
                                                                            text= "ခနစောင့် ကွာ ....",
                                            
                                                                            )	

                                        width = 100
                                        height = 100
                                        duration = 0
                                        metadata = extractMetadata(createParser(file_path))
                                        if metadata.has("duration"):
                                            duration = metadata.get('duration').seconds
                                        if metadata.has("width"):
                                            width = metadata.get("width")
                                        if metadata.has("height"):
                                                height = metadata.get("height")	
                                        posterfile = os.path.basename(posterurl)
                                        video_thumbnails = DOWNLOAD_DIRECTORY + str(message.from_user.id) + "/" + "thumb.jpg"
                                        file_size = os.path.getsize(file_path)
                                        if (int(file_size) > 2097152000):
                                            await bot.send_message(
                                                                chat_id=message.chat.id,
                                                                text= "We Cannot upload",
                                                    )
                                        #sent_vid = await send_video_handler_fmax(bot, message, file_path, video_thumbnails, duration, width, height, editable, file_size, title)
                                        sent_vid = await send_video_channel(bot, chid, file_path, video_thumbnails, duration, width, height, editable, file_size, title)
                                                            #msg = GoogleDrive(user_id).upload_file(file_path)
                                                            #sent_message.edit(msg)
                                                            #LOGGER.info(f'Deleteing: {file_path}')
                                                            #os.remove(file_path)
                                        
                                        await editable.delete()
                                        os.remove(video_thumbnails)
                                        filelist = glob.glob(os.path.join(dl_path, "*.*"))
                                        for f in filelist:
                                            os.remove(f)
                                else:
                                    sent_message = await message.reply_text('🕵️**လီး လို လို ပဲ လွဲ နေ ပြီ ..ငလူးမ မိုးဒီယူ ကို အကြောင်း ကြား နွားလေး **', quote=True)
    else:
        await message.reply_text(
                            text="တစ်ခုခုတော့ ရှာလေကွာ ... "    
                            )