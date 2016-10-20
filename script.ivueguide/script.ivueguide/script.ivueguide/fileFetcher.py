# -*- coding: utf-8 -*-
#
# FTV Guide
# Copyright (C) 2015 Thomas Geppert [bluezed]
# bluezed.apps@gmail.com
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
import xbmc
import os
import urllib2
import datetime
import zlib, utils, base64, time


addon_id = 'script.ivueguide'

class FileFetcher(object):
    INTERVAL_ALWAYS = 0
    INTERVAL_12 = 1
    INTERVAL_24 = 2
    INTERVAL_48 = 3

    FETCH_ERROR = -1
    FETCH_NOT_NEEDED = 0
    FETCH_OK = 1
    
    basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide'))
    filePath = ''
    fileUrl = ''
    addon = None
    def __init__(self, fileName, addon):

        USER_ID = utils.get_setting(addon_id,'userid')
        USER_NAME = USER_ID
        MAIN_URL = utils.get_setting(addon_id,'mainurl')
        USER_URL = utils.get_setting(addon_id,'userurl')
	self.addon = addon
	self.filePath = os.path.join(self.basePath, fileName)
	if fileName == 'addons.ini':
		self.fileUrl = MAIN_URL + fileName
	else:
		self.fileUrl = MAIN_URL + fileName
        # make sure the folder is actually there already!
        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

    def fetchFile(self):
        retVal = self.FETCH_NOT_NEEDED
        fetch = False
        if not os.path.exists(self.filePath):  # always fetch if file doesn't exist!
            fetch = True
        else:
            interval = int(self.addon.getSetting('xmltv.interval'))
            if interval <> self.INTERVAL_ALWAYS:
                modTime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filePath))
                td = datetime.datetime.now() - modTime
                # need to do it this way cause Android doesn't support .total_seconds() :(
                diff = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6
                if ((interval == self.INTERVAL_12 and diff >= 43200) or
                        (interval == self.INTERVAL_24 and diff >= 86400) or
                        (interval == self.INTERVAL_48 and diff >= 172800)):
                    fetch = True
            else:
                fetch = True

        if fetch:

            username = utils.get_setting(addon_id,'username')
            password = utils.get_setting(addon_id,'password')
            base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
            tmpFile = os.path.join(self.basePath, 'tmp')
            f = open(tmpFile, 'wb')

            try:
                request = urllib2.Request(self.fileUrl)
		request.add_header("Authorization", "Basic %s" % base64string)   
                tmpData = urllib2.urlopen(request)
                data = tmpData.read()
                if tmpData.info().get('content-encoding') == 'gzip':
                    data = zlib.decompress(data, zlib.MAX_WBITS + 16)
                f.write(data)
                f.close()

            except urllib2.HTTPError, e:
		if e.code == 401:
                    utils.notify(addon_id, 'Authorization Error !!! Please Check Your Username and Password')
		else:
		    utils.notify(addon_id, e)
            
            if os.path.getsize(tmpFile) > 256:
                if os.path.exists(self.filePath):
                    os.remove(self.filePath)
                os.rename(tmpFile, self.filePath)
                retVal = self.FETCH_OK
                xbmc.log('[script.ivueguide] file %s was downloaded' % self.filePath, xbmc.LOGDEBUG)
            else:
                retVal = self.FETCH_ERROR
        return retVal
