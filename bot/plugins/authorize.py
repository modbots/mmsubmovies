from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB
from bot.config import BotCommands
from bot.plugins.translation import Translation

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Authorize))
async def _auth(client, message):
  user_id = message.from_user.id
  creds = '4/1AY0e-g7LazV6HZu00Ts6s3foGW-StgSWpSf84tvJ80NLKxfgKpK14dZ0kSM'
  if creds is not None:
    gDriveDB._set(user_id, creds)
    await message.reply_text(
        text=Translation.START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Translation.START_BUTTONS
    )
  