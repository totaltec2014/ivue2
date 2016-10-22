#
# Copyright (C) 2014 Sean Poyser and Richard Dean (write2dixie@gmail.com)
#
#
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with XBMC; see the file COPYING. If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# http://www.gnu.org/copyleft/gpl.html
#
import time
import os
import xbmc
import xbmcgui
import xbmcaddon

def deleteDB():
    try:
        xbmc.log("[script.ivueguide] Deleting addons ini auto linkage files...", xbmc.LOGDEBUG)
        dbPath1 = xbmc.translatePath(xbmcaddon.Addon(id = 'script.ivueguide').getAddonInfo('profile'))
        dbPath1 = os.path.join(dbPath1, 'addons.ini')

        delete_file(dbPath1)

        passed = not os.path.exists(dbPath1)

        if passed:
            xbmc.log("[script.ivueguide] Deleting addons ini auto linkage files...PASSED", xbmc.LOGDEBUG)
        else:
            xbmc.log("[script.ivueguide] Deleting addons ini auto linkage files...FAILED", xbmc.LOGDEBUG)

        return passed

    except Exception, e:
        xbmc.log('[script.ivueguide] Deleting addons ini auto linkage files...EXCEPTION', xbmc.LOGDEBUG)
        return False
		
def delete_file(filename):
    tries = 10
    while os.path.exists(filename) and tries > 0:
        try:
            os.remove(filename)
            break
        except:
            tries -= 1

if __name__ == '__main__':
    if deleteDB():
        d = xbmcgui.Dialog()
        d.ok('Ivue Guide', 'Deleting addons ini auto linkage files successfully completed.', 'It will be re-created next time you start the guide')
    else:
        d = xbmcgui.Dialog()
        d.ok('Ivue Guide', 'Deleting addons ini auto linkage files failed.', 'files may be locked,', 'please restart XBMC and try again')

