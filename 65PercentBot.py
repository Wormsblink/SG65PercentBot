#import default python modules
from datetime import datetime
import time
import traceback

#import other modules
import login
import getlists
import bot
import config

r = login.bot_login()


while True:
   try:
       bot.run_bot(r)
       time.sleep(10)
   except Exception as err:
       print(traceback.format_exc())
       print("Fatal error at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ", " + str(err))
       time.sleep(3600)
