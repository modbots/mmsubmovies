from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Translation(object):

    START_TEXT = """
မင်္ဂလာပါ  {}  ကျတော်က တော့ ချန်နယ် ဘော့ပါ အရာအားလုံးတော်တော်များများကို ဖေဖေ သင်ပေထားပါတယ်

Made by @moedyiu
"""
    CM_DES = """
မင်္ဂလာပါ  {} , ခင်ဗျားဘာကို ရှာချင်တာလဲ.

Made by @moedyiu
"""
    HELP_TEXT = """
I cannot help you 😌

Made by @moedyiu
"""
    ABOUT_TEXT = """
- **Bot :** `MMSUB CHANNEL BOT`
- **Creator :** [Moedyiu](https://telegram.me/moedyiu)
- **Channel :** [Moedyiu](https://telegram.me/moedyiu)
- **Credits :** `Everyone in this journey`
- **Source :** [Click here](https://github.com/modbots)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram v1.2.0](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)
""" 
    FETCH_BUTTONS = InlineKeyboardMarkup(
             
       [[ InlineKeyboardButton('FETCH NOW', callback_data='fetch')]]
    )  

    VS_BUTTONS = InlineKeyboardMarkup(
             
       [[ InlineKeyboardButton('UPLOAD ON YOUR CHANNEL', callback_data='vsdown')]]
    )  

    DES_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('ONLY VIDEO', callback_data='vidonly'),
        InlineKeyboardButton('ONLY DESCRIPTION', callback_data='desonly')
        ],
        [
        InlineKeyboardButton('BOTH VIDEO + DESCRIPTION', callback_data='bothviddes')]]
    )  
    MDES_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('ONLY VIDEO', callback_data='mmvidonly'),
        InlineKeyboardButton('ONLY DESCRIPTION', callback_data='mmdesonly')
        ],
        [
        InlineKeyboardButton('BOTH VIDEO + DESCRIPTION', callback_data='mmbothviddes')]]
    )  
    
    START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
    FORMAT_SELECTION = """<b>Select the desired format:</b> <a href='{}'>file size might be approximate</a>
    
Send your custum thumbnail if required.
You can use /delthumb to delete the auto-generated thumbnail."""
    CHECKING_LINK = "<code>Analysing Your Link</code>⏳"
    BANNED_USER_TEXT = "<code>You are Banned!</code>"
    SET_CUSTOM_USERNAME_PASSWORD = """If you want to download premium videos, provide in the following format:
URL | newfilename | username | password"""
    DOWNLOAD_START = "<code>Downloading To My server Please Wait...</code>"    
    UPLOAD_START = "<code>Uploading into Telegram...</code>"
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "Downloaded in {} seconds. \n\nUploaded in {} seconds."
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 1.95GB due to Telegram API limitations."
    CUSTOM_CAPTION_UL_FILE = "<b>Join :-</b> @FayasNoushad"
    SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Since you were screwing my home, I am in no mood to download this file. Meanwhile, why don't you try this:==> https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
    NO_VOID_FORMAT_FOUND = "<code>{}</code>"
    REPORT_SITE_TEXT = "<code>Sorry not uploading in this site here because this site is reporting site.</code>"
    SOMETHING_WRONG = "<code>Something Wrong. Try again.</code>"
    FORCE_SUBSCRIBE_TEXT = "<code>Sorry Dear You Must Join My Updates Channel for using me 😌😉....</code>"
    FREE_USER_LIMIT_Q_SZE = "Sorry Friend, Free users can only 1 request per {} minutes. Please try again after {} seconds later."
