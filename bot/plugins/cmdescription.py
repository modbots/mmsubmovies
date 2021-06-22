from pyrogram.methods.messages import send_message
import requests 
import bs4 
import wget
import os
from pyrogram import Client, filters
from bot.config import BotCommands
from myanmartools import ZawgyiDetector
from bot import LOGGER
from bot.zgconvert import zg_convert
from bot.plugins.translation import Translation
from bot.helpers.sql_helper import urldb

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Channelmyanmar) )
async def cmdescription(client, message):
    user_id = message.from_user.id
    if len(message.command) > 1:
        search = message.text.split(' ',maxsplit=1)[1]
        sent_message =await message.reply_text('🕵️** Searching on Channelmyanmar .Please Wait ...**', quote=True)
        LOGGER.info(f'CMDESCP:{user_id}: {search}')
        url = "https://channelmyanmar.org/?s=" + search 
        request_result = requests.get( url )
        soup = bs4.BeautifulSoup( request_result.text 
                                , "html.parser" )
        if not 'No content available' in soup:
            URLs=[] 
            mydivs = soup.find_all("div", {"class": "boxinfo"})
            desp = soup.find("span", {"class": "ttx"})
            for div in mydivs:
                links = div.findAll('a')
                for a in links:
                    newUrl = a['href']
                if len(URLs) <= 0:
                    URLs.append(newUrl)
            cmlink = str(URLs).replace("['", " ").replace("']", " ")
            desps = str(desp).replace('<span class="ttx">', ' ').replace('<div class="degradado"></div>', ' ').replace('</span>', ' ')
            noon = "None"
            if not os.path.exists("pb.txt"):
                wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
            pb = open("pb.txt", 'r')
            for l in pb:
                l = l.strip()
            if desps == noon:
                cm_noon = "I cannot find it on channelmyanmar.org ..."
                await sent_message.edit(cm_noon)
            else:
                msg_id = message.message_id
                cb_msg_id = int(msg_id + 2)
                urldb._set(cb_msg_id, search)
                cm_desp = desps + cmlink + "\n" + l
                detector = ZawgyiDetector()
                score = detector.get_zawgyi_probability(desps)
                if score > 0.7 :
                    cm_desp = zg_convert(cm_desp)
                    await sent_message.delete()
                    await message.reply_text(
                            text=cm_desp.format(message.from_user.mention),
                            disable_web_page_preview=True,
                            reply_markup=Translation.DES_BUTTONS
                            )
                else:
                    
                    chid = urldb.search_url(user_id)
                    
                        
                    if chid == "NOON":
                        await sent_message.delete()
                        await message.reply_text(
                            text="Please Give Me Your Channel ID first \nUSAGE: /chid your channel id (-10054545454)... "    
                            )
                    else:
                        await sent_message.delete() 
                        
                                        
                        await message.reply_text(
                                text=cm_desp.format(message.from_user.mention),
                                disable_web_page_preview=True,
                                reply_markup=Translation.DES_BUTTONS
                                )
    else:
        await message.reply_text(
                            text="Please Find Something \nUSAGE: /cm movie name(lone ranger) ... "    
                            )








def cmlinkfetch(movies):
#    sent_message = movies.reply_text('🕵️**Checking Channelmyanmar link...**', quote=True)
    LOGGER.info(f'FETCHING: cmlink')
    url = "https://channelmyanmar.org/?s=" + movies
    request_result = requests.get( url )
    soup = bs4.BeautifulSoup( request_result.text 
                            , "html.parser" )
    if not 'No content available' in soup:
        URLs=[] 
        mydivs = soup.find_all("div", {"class": "boxinfo"})
        desp = soup.find("span", {"class": "ttx"})
        for div in mydivs:
            links = div.findAll('a')
            for a in links:
                newUrl = a['href']
            if len(URLs) <= 0:
                URLs.append(newUrl)
        cmlink = str(URLs).replace("['", " ").replace("']", " ") 
        desps = str(desp).replace('<span class="ttx">', ' ').replace('<div class="degradado"></div>', ' ').replace('</span>', ' ')
        noon = "None"
        if not os.path.exists("crd.txt"):
            wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
        pb = open("pb.txt", 'r')
        for l in pb:
            l = l.strip()
        if desps == noon:
            cm_noon = "No such movies on channelmyanmar.org ..."
            cm_desp = cm_noon
            return cm_desp
        else:
            cm_desp = desps + cmlink + "\n" + l
            detector = ZawgyiDetector()
            score = detector.get_zawgyi_probability(desps)
            if score > 0.7 :
                cm_desp = zg_convert(cm_desp)
                return cm_desp
            else:
                return cm_desp
        
            
async def desonly(bot, update, search,userid):
#    sent_message = movies.reply_text('🕵️**Checking Channelmyanmar link...**', quote=True)
    LOGGER.info(f'FETCHING: {search}')
    url = "https://channelmyanmar.org/?s=" + search 
    request_result = requests.get( url )
    soup = bs4.BeautifulSoup( request_result.text 
                            , "html.parser" )
    chid = urldb.search_url(userid)
    if not 'No content available' in soup:
        URLs=[] 
        mydivs = soup.find_all("div", {"class": "boxinfo"})
        desp = soup.find("span", {"class": "ttx"})
        for div in mydivs:
            links = div.findAll('a')
            for a in links:
                newUrl = a['href']
            if len(URLs) <= 0:
                URLs.append(newUrl)
        cmlink = str(URLs).replace("['", " ").replace("']", " ") 
        desps = str(desp).replace('<span class="ttx">', ' ').replace('<div class="degradado"></div>', ' ').replace('</span>', ' ')
        noon = "None"
        if not os.path.exists("crd.txt"):
            wget.download('https://raw.githubusercontent.com/modbots/backen/main/pb.txt')
        pb = open("pb.txt", 'r')
        for l in pb:
            l = l.strip()
        
        if desps == noon:
            cm_noon = "No such movies on channelmyanmar.org ..."
            cm_desp = cm_noon
            return cm_desp
        else:
            cm_desp = desps + cmlink + "\n" + l
            detector = ZawgyiDetector()
            score = detector.get_zawgyi_probability(desps)
            if score > 0.7 :
                cm_desp = zg_convert(cm_desp)
                
                await bot.send_message(
                            chat_id=chid,
                            text=cm_desp
                            )
            else:
                await bot.send_message(
                            chat_id=chid,
                            text=cm_desp
                            )
            await bot.send_message(     chat_id=userid,
                                            text= "Already Sent To Your Channel... ",
                    
                                )
        
            
        
            
        
