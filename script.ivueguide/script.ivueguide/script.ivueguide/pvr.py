# -*- coding: utf-8 -*-

# Deleting this file cripples the entire addon

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
# http://kodi.wiki/view/How-to:Write_Python_Scripts
################################################

from __future__ import unicode_literals
from collections import namedtuple
import codecs
import sys,os,json,urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re
import shutil
import base64
import xbmcvfs
import urllib
import random
import hashlib
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import cookielib
import pickle
import time
import datetime


addon         = 'script.ivueguide'
ADDONID       = addon
addon_name    = addon
addonPath     = xbmc.translatePath(os.path.join('special://home/addons', addon))
basePath      = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon))
tmp_File      = os.path.join(basePath, 'tmp.ini')
icon          = xbmc.translatePath(os.path.join('special://home/addons', addon, 'icon.png'))
dbPath        = xbmc.translatePath(xbmcaddon.Addon(addon).getAddonInfo('profile'))
dialog        = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()

inipath       = xbmc.translatePath(os.path.join(basePath, 'resources', 'ini'))

if not os.path.exists(basePath):
    os.makedirs(basePath)
            
if not os.path.exists(os.path.join(basePath, 'resources')):
    os.makedirs(os.path.join(basePath, 'resources'))
def notify(header,msg,icon_path):
    duration=2000
    xbmcgui.Dialog().notification(header, msg, icon=icon_path, time=duration, sound=False)
def validTime(setting, maxAge):
    previousTime = getPreviousTime(setting)
    now          = datetime.datetime.today()
    delta        = now - previousTime
    nSeconds     = (delta.days * 86400) + delta.seconds
    return nSeconds <= maxAge     
def SetSetting(param, value):
    value = str(value)
    if GetSetting(param) == value:
        return
    xbmcaddon.Addon(addon).setSetting(param, value)
def DialogOK(line1, line2='', line3=''):
    d = xbmcgui.Dialog()
    d.ok('Subscriptions', line1, line2 , line3)     
def log(text):
    try:
        output = '%s V%s : %s' % ("Log", 'Error?', str(text))
        if DEBUG:
            xbmc.log(output)
        else:
            xbmc.log(output, xbmc.LOGDEBUG)
    except: pass

def StartCreate():


    if os.path.exists(inipath):
        shutil.rmtree(inipath)
    if not os.path.exists(inipath):
        os.makedirs(inipath)
                           

    add_pvr()

    return

def add_pvr():
    iniFle = 'pvr.ini';writestyle = 'w'
    iniPvrAddonName = 'script.ivueguide'
    #iniPvrAddonName = 'pvr.iptvsimple'
    #
    PVRACTIVE   = (xbmc.getCondVisibility('Pvr.HasTVChannels')) or (xbmc.getCondVisibility('Pvr.HasRadioChannels')) == True    
    if not PVRACTIVE:
        return       
    pvrinipath  = os.path.join(inipath, iniFle)
    notify('PVR',iniFle,os.path.join(addonPath, 'resources', 'png', 'pvr.png'))##NOTIFY##
    
    try:
        tryTvChannels  = _getPVRChannels('"tv"')
        tryTvChannelsCommand = tryTvChannels['result']          
    except: pass   
    
    try:
        tryRadio  = _getPVRChannels('"radio"')
        tryRadioCommand = tryRadio['result']
    except: pass
    
    try:
        foundTvChannels  = tryTvChannelsCommand['channels']      
        foundRadioChannels  = tryRadioCommand['channels']
    except: pass    
    ThePVRini  = file(pvrinipath, writestyle)    
    ThePVRini.write('['+iniPvrAddonName+']\n')       
    try:
        for TryToFindStreams in foundTvChannels:
            WhatsTheGroupID  = TryToFindStreams['label']  
            stream = ('%s') % TryToFindStreams['channelid']
            ThePVRini.write('%s' % WhatsTheGroupID)
            ThePVRini.write("=")
            ThePVRini.write(('%s') % stream)            
            ThePVRini.write("\n")
    except: pass    
    try:
        for TryToFindStreams in foundRadioChannels:          
            WhatsTheGroupID  = TryToFindStreams['label']  
            stream = ('%s') % TryToFindStreams['channelid']
            ThePVRini.write('%s' % WhatsTheGroupID)
            ThePVRini.write("=")
            ThePVRini.write('%s' % stream)            
            ThePVRini.write("\n")
    except: pass   
    ThePVRini.write("\n")
    ThePVRini.close()

def _getPVRChannels(group):   
    method   = 'PVR.GetChannels'
    params   = 'channelgroupid'
    WhatAreGroupIDs  =  getGroupID(group)
    checkPVR =  sendJSONpvr(method, params, WhatAreGroupIDs)   
    return checkPVR
#
def getGroupID(group):
    method   = 'PVR.GetChannelGroups'
    params   = 'channeltype'   
    checkPVR = sendJSONpvr(method, params, group)
    result   = checkPVR['result']
    groups   = result['channelgroups']
    #
    for group in groups:
        WhatsTheGroupID = group['label']
        if WhatsTheGroupID == 'All channels':
            return group['channelgroupid']
#
def sendJSONpvr(method, params, value):
    JSONPVR  = ('{"jsonrpc":"2.0","method":"%s","params":{"%s":%s}, "id":"1"}' % (method, params, value))    
    checkPVR = xbmc.executeJSONRPC(JSONPVR)
    return json.loads(checkPVR.decode("utf-8"),"ignore")
# PVR End #

def Clean_Names(Clean_Name,tmpFile):
    if os.path.exists(tmpFile):
        os.remove(tmpFile)
    os.rename(Clean_Name, tmpFile)
    s=open(tmpFile).read()
    s=s.replace('','') 
    f=open(Clean_Name,'a')
    f.write(s)
    f.close()
    os.remove(tmpFile)
    return

if __name__ == '__main__':
    if StartCreate():
        StartCreate()
        print 'Subscriptions1'
    else:
        print 'Subscriptions2'