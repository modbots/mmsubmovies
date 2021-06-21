class config:
    BOT_TOKEN = "1406408953:AAHjcYwC1Jsu4bYCwg4cO4EIBesXmwSNJTQ"
    APP_ID = "1438968"
    API_HASH = "c0f0b02b10b2f31bdd15044d761de4e5"
    #DATABASE_URL = "postgresql://bmwjnovswckjdq:76f9a4bfff1022c099b9bcc3a46ce86aa62b354ee971fb305941e0eb6bacfbab@ec2-34-193-112-164.compute-1.amazonaws.com:5432/df461p1bahc74h"
    DATABASE_URL = "postgres://vgmnajoalaxstm:0c97e2da0939c7d22f031c1fe76b37480f783988f6c9992c9669bf79a0fa3519@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d6h3sdvkki1b5n"
    
    SUDO_USERS = "1247136776" # Sepearted by space.
    SUPPORT_CHAT_LINK = "t.me/moedyiu"
    DOWNLOAD_DIRECTORY = "./downloads/"
    PROGRESS = """
Percentage : {0}%
Done ✅: {1}
Total 🌀: {2}
Speed 🚀: {3}/s
ETA 🕰: {4}
"""


class BotCommands:
  Authorize = ['auth', 'start']
  Delete = ['delete', 'del']
  EmptyTrash = ['emptyTrash']
  Channelmyanmar = ['cm']
  Mmsubtitles = ['mmsub']
  Vidsearch = ['vid']
  Linkgen = ['cmgen']
  Logo = ['logo']
  Javgen = ['javgen']
  Test = ['test']
class Messages:
    
    NOT_AUTH = f"🔑 **You have not authenticated me to upload to any account.**\n__Send /{BotCommands.Authorize[0]} to authenticate.__"
    START = "တင်‌ပေးနေပါပြီနော် "
    DOWNLOADED_SUCCESSFULLY = "📤 **mmsub.co...**\n**Filename:** ```{}```\n**Size:** ```{}```"
    
    
