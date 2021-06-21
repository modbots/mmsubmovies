import requests 
import bs4 
import os
import wget
from pyrogram import Client, filters
from bot.config import BotCommands, Messages
from bot.helpers.utils import CustomFilters
from bot.helpers.gdrive_utils import GoogleDrive
from myanmartools import ZawgyiDetector
from bot import LOGGER
from bot.zgconvert import mmsub_desp
from bot.plugins.translation import Translation
from bot.helpers.sql_helper import urldb
@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Mmsubtitles) )

async def mmsub(client, message):
    user_id = message.from_user.id
    search = message.text.split(' ',maxsplit=1)[1]
    msg_id = message.message_id
    cb_msg_id = int(msg_id + 1)
    urldb._set(cb_msg_id, search)
    LOGGER.info(f'MMSUB:{user_id}: {search}')
    url = "https://mmsubtitles.co/?s=" + search
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup( request_result.text 
                            , "html.parser" )
    mydivs = soup.find_all("div", {"class": "no-result animation-2"})
    if mydivs == []:
        URLs=[] 
        mydivs = soup.find_all("div", {"class": "thumbnail animation-2"})
        #desp = soup.find("span", {"class": "ttx"})
        for div in mydivs:
            links = div.findAll('a')
            for a in links:
                newUrl = a['href']
            if len(URLs) <= 0:
                URLs.append(newUrl)
        mmsublink = str(URLs).replace("['", " ").replace("']", " ")
        if not os.path.exists("pb.txt"):
                wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
        pb = open("pb.txt", 'r')
        for l in pb:
            l = l.strip()        
        descp = mmsub_desp(mmsublink)
        await client.send_message(
                            chat_id=user_id,
                            text= descp + '\n' + l ,
                            disable_web_page_preview=True,
                            reply_markup=Translation.MDES_BUTTONS
                            )
        
    else:
        await client.send_message(
                            chat_id=user_id,
                            text= "ကျနော်ရှာကြည့်တာ  mmsubtitles.co မှာ ခင်ဗျားရှာတာ မတွေ့ပါဘူးဗျာ.."
                            
                            )

async def mmsubonly(client, message,search, user_id):
    LOGGER.info(f'MMSUB:{user_id}: {search}')

    url = "https://mmsubtitles.co/?s=" + search
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup( request_result.text 
                            , "html.parser" )
    mydivs = soup.find_all("div", {"class": "no-result animation-2"})
    if mydivs == []:
        URLs=[] 
        mydivs = soup.find_all("div", {"class": "thumbnail animation-2"})
        #desp = soup.find("span", {"class": "ttx"})
        for div in mydivs:
            links = div.findAll('a')
            for a in links:
                newUrl = a['href']
            if len(URLs) <= 0:
                URLs.append(newUrl)
        mmsublink = str(URLs).replace("['", " ").replace("']", " ")
        if not os.path.exists("pb.txt"):
                wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
        pb = open("pb.txt", 'r')
        for l in pb:
            l = l.strip()        
        descp = mmsub_desp(mmsublink) + '\n' + l
        chid = urldb.search_url(user_id)
        await client.send_message(chat_id=chid,
                            text=descp
                            )
        await client.send_message(     chat_id=user_id,
                                            text= "သင့်ချန်နယ်ပေါ် တင်ပြီးပါပြီ ",
                    
                                )
    