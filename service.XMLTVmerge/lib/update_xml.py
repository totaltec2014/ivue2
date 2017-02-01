import os
from common_variables import *
from xmltvmerger import *
xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('XMLTVmerge', "Merging EPG's. Wait...", 1,os.path.join(addonfolder,"icon.png")))
xml_merge(notification=True)
