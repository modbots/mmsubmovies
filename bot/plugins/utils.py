import os
import shutil
from os import execl
from time import sleep
from sys import executable
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from bot import SUDO_USERS, DOWNLOAD_DIRECTORY, LOGGER, SUPPORT_CHAT_LINK
from bot.config import Messages as tr
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.plugins.translation import Translation
from bot.helpers.sql_helper import urldb
from bot.helpers.sql_helper import chidds
from bot.plugins.vidsearch import download_vid
from bot.plugins.cmdescription import desonly

@Client.on_message(filters.private & filters.incoming & filters.command(['chid']) )
async def cmdescription(client, message):
    user_id = message.from_user.id
    
    if len(message.command) > 1:
    
        chid = message.text.split(' ',maxsplit=1)[1]
        
        urldb._set(user_id, chid)
        results = urldb.search(user_id, chid)
        await message.reply_text(
            text="ခင်ဗျား ချန်နယ်ကို ကျနော် အသိအမှတ်ပြု လိုက်ပါပြီ" + str(results),
            disable_web_page_preview=True,
            )
        

@Client.on_message(filters.private & filters.incoming & filters.command(['log']) & filters.user(SUDO_USERS))
def _send_log(client, message):
  with open('log.txt', 'rb') as f:
    try:
      client.send_document(
        message.chat.id,
        document=f,
        file_name=f.name,
        reply_to_message_id=message.message_id
        )
      LOGGER.info(f'Log file sent to {message.from_user.id}')
    except FloodWait as e:
      sleep(e.x)
    except RPCError as e:
      message.reply_text(e, quote=True)

@Client.on_message(filters.private & filters.incoming & filters.command(['restart']) & filters.user(SUDO_USERS))
def _restart(client, message):
  shutil.rmtree(DOWNLOAD_DIRECTORY)
  LOGGER.info('Deleted DOWNLOAD_DIRECTORY successfully.')
  message.reply_text('**♻️Restarted Successfully !**', quote=True)
  LOGGER.info(f'{message.from_user.id}: Restarting...')
  execl(executable, executable, "-m", "bot")



@Client.on_message(filters.command(["starts"]) & filters.private)
async def start(bot, update):
    
    await update.reply_text(
        text=Translation.START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Translation.START_BUTTONS
    )

@Client.on_callback_query()
async def button(bot, update):
    if update.data == "help":
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=Translation.HELP_BUTTONS,
            disable_web_page_preview=False
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=Translation.ABOUT_TEXT,
            reply_markup=Translation.ABOUT_BUTTONS,
            disable_web_page_preview=False
        )
    elif update.data == "vidonly":
        user_id = update.from_user.id
        cb_msg_id = update.message.message_id
        search = urldb.search_url(cb_msg_id)
        await download_vid(bot, update, search, str(user_id))
    elif update.data == "desonly":
        user_id = update.from_user.id
        cb_msg_id = update.message.message_id
        search = urldb.search_url(cb_msg_id)
        await desonly(bot, update, search, str(user_id))
    elif update.data == "bothviddes":
        user_id = update.from_user.id
        cb_msg_id = update.message.message_id
        search = urldb.search_url(cb_msg_id)
        await desonly(bot, update, search, str(user_id))
        await download_vid(bot, update, search, str(user_id))
    else:
        await update.message.delete()

    
        


