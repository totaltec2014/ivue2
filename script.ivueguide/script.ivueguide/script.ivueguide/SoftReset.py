import time
import os
import xbmc
import xbmcgui
import xbmcaddon

databasePath = xbmc.translatePath('special://userdata/addon_data/script.ivueguide')
d = xbmcgui.Dialog()

			
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "guides.ini" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "addons.ini" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "addons2.ini" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "guide.xml" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "amylist.xml" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "teamexpat.xml" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "otttv.xml" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "guide2.xml" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "uk3.xml" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "guide3.xmltv" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
						
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "master.xml" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				pass
		else:
			continue
			
d = xbmcgui.Dialog()			
d.ok('Ivue guide Soft reset', 'Please restart for ','the changes to take effect','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
