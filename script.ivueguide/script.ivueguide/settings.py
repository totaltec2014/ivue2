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
import xbmcgui, utils

addon_id = 'script.ivueguide'
dlg = xbmcgui.Dialog()


def showTOS():
	tos = utils.get_setting(addon_id,'tos')== "true"
#	if tos == False:
#		utils.set_setting(addon_id, 'tos', 'true')
#		dlg.ok('IVUE TV Guide TOS','By using Ivue Guide you agree to the terms and conditions found at https://www.facebook.com/groups/tecbox')

def setSettings(username,password,userid):
       username = utils.set_setting(addon_id, 'username', username)
       password = utils.set_setting(addon_id, 'password', password)
       userid = utils.set_setting(addon_id, 'userid', userid)

def setUrl():
	user = utils.set_setting(addon_id, 'userurl', 'http://ivuetvguide.com/ivueguide/') 
	url = utils.set_setting(addon_id, 'mainurl', 'http://ivuetvguide.com/ivueguide/')
	logos = utils.set_setting(addon_id, 'logos', 'http://ivuetvguide.com/ivueguide/logos/')	
	   
def checkSettings():
        username = utils.get_setting(addon_id,'username')
        password = utils.get_setting(addon_id,'password')
        userid = utils.get_setting(addon_id,'userid')
        if not username:
                retval = dlg.input('Enter Ivue Guide Username', type=xbmcgui.INPUT_ALPHANUM)
                if retval and len(retval) > 0:
                        utils.set_setting(addon_id, 'username', str(retval))
                        username = utils.get_setting(addon_id, 'username')
        
        if not password:
                retval = dlg.input('Enter Ivue Guide Password', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                if retval and len(retval) > 0:
                        utils.set_setting(addon_id, 'password', str(retval))
                        password = utils.get_setting(addon_id, 'password')
		
        if not userid:
                retval = dlg.input('Enter Ivue Guide UserID', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                if retval and len(retval) > 0:
                        utils.set_setting(addon_id, 'userid', str(retval))
                        userid = utils.get_setting(addon_id, 'userid')

