import requests
import os
from requests import get
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint
from pyrogram import Client, filters
from bot.config import BotCommands, Messages
from bot.helpers.utils import CustomFilters
from bot.plugins.translation import Translation

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Linkgen))
async def mmsub(bot, message):
  user_id = message.from_user.id
  if len(message.command) > 1:
    editable = await bot.send_message(
                                                  chat_id=message.chat.id,
                                                  text= "ရှာဖွေနေပါသည်",
                                      )
    search = message.text.split(' ',maxsplit=1)[1]
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    pages = np.arange(int(search))

    if os.path.exists(str(user_id) + ".txt"):
      os.remove(str(user_id) + ".txt")
    for page in pages: 
      page = requests.get("https://channelmyanmar.org/movies/page/" + str(page), headers=headers)
      soup = BeautifulSoup(page.text, 'html.parser')
      movie_div = soup.find_all('div', class_='boxinfo')
      sleep(randint(2,10))
      URLs=[]
      for div in movie_div:
        links = div.findAll('a')
        for a in links:
            newUrl = a['href']
        if len(URLs) <= 21:
            URLs.append(newUrl)
      s = ', '.join(map(str,URLs)).replace(',','\n').replace(' ', '') 
      with open(str(user_id) + ".txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(s)

    with open(str(user_id) + ".txt", 'rb') as f:
        await editable.delete()
        await bot.send_document(document=f,
                          reply_to_message_id=message.message_id,
                          chat_id=message.from_user.id,
                          reply_markup=Translation.FETCH_BUTTONS)
  else:
        await message.reply_text(
                            text="တစ်ခုခုတော့ ရှာလေကွာ.. /cmgen 9  ... "    
                            )