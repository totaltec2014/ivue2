#      Copyright (C) 2015 Justin Mills
#      
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import sys, urllib,urllib2, urlparse, os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

	#Plays a video
def playMedia(name, image, link, mediaType='Video') :
    li = xbmcgui.ListItem(label=name, iconImage=image, thumbnailImage=image, path=link)
    li.setInfo(type=mediaType, infoLabels={ "Title": name })
    xbmc.Player().play(item=link, listitem=li)

	#Add a menu item to the xbmc GUI
def addMenuItem(name, url, playable ='0', fanart=None, icon=None, thumbnail=None, folder=False):		
	listItem = xbmcgui.ListItem(unicode(name), iconImage=icon, thumbnailImage=thumbnail)
	listItem.setInfo(type="Video", infoLabels={ "Title": name})
	listItem.setProperty('fanart_image', fanart)
	if playable in ['1', 'Yes']:
		listItem.setProperty('IsPlayable', 'true')
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listItem, isFolder=folder)

	#Signals the end of the menu listing
def endListing():
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

	#Displays a notification to the user
def notify(addonId, message, timeShown=5000):
    addon = xbmcaddon.Addon(addonId)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))

	#Shows an error to the user and logs it
def showError(addonId, errorMessage):
    notify(addonId, errorMessage)
    xbmc.log(errorMessage, xbmc.LOGERROR)

	#Download a file url/file to save
def download_file(url,file):
    urllib.urlretrieve(url, file)

	#Create user addon directory
def create_userdata(AddOnID):
    addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddOnID)
    if not os.path.exists(addon_data_dir):
        os.makedirs(addon_data_dir)	
		
def get_setting(addonId,setting):
	addon = xbmcaddon.Addon(addonId)
	return addon.getSetting(setting)
    
def set_setting(addonId,setting, string):
	addon = xbmcaddon.Addon(addonId)
	return addon.setSetting(setting, string)