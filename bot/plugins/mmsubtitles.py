import requests 
import bs4 
from pyrogram import Client, filters
from bot.config import BotCommands, Messages
from bot.helpers.utils import CustomFilters
from bot.helpers.gdrive_utils import GoogleDrive
from myanmartools import ZawgyiDetector
from bot import LOGGER
from bot.zgconvert import mmsub_desp
@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Mmsubtitles) )

def mmsub(client, message):
    user_id = message.from_user.id
    search = message.text.split(' ',maxsplit=1)[1]
    sent_message = message.reply_text('🕵️**Checking Channelmyanmar link...**', quote=True)
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
        descp = mmsub_desp(mmsublink)
        sent_message.edit(descp)
    else:
        sent_message.edit("ကျနော်ရှာကြည့်တာ  mmsubtitles.co မှာ ခင်ဗျားရှာတာ မတွေ့ပါဘူးဗျာ..")
    