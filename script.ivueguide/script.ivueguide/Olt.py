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
m3upath       = xbmc.translatePath(os.path.join(basePath, 'resources', 'm3u'))
Olt           = 'plugin.video.overlordtv'


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
  
    if os.path.exists(basePath + '/playlist.m3u'):
        os.remove(basePath + '/playlist.m3u')


    if os.path.exists(inipath):
        shutil.rmtree(inipath)
    if not os.path.exists(inipath):
        os.makedirs(inipath)
              
    if not os.path.exists(m3upath):
        os.makedirs(m3upath)
        
     

    add_pvr()
    add_Oltini()

    return


def add_Oltini():
    TheseAddons   =  [Olt]#Jules: only run for Olt!!
    for FoundAddon in TheseAddons:
        if CheckHasThisAddon(FoundAddon):
            notify('generating channels',FoundAddon,os.path.join('special://home/addons', FoundAddon, 'icon.png'))##NOTIFY##
            ParseOltData(FoundAddon)
def CheckHasThisAddon(FoundAddon):
    if xbmc.getCondVisibility('System.HasAddon(%s)' % FoundAddon) == 1:
        settingsFileCheck = xbmc.translatePath(os.path.join('special://home/userdata/addon_data',FoundAddon,'settings.xml'))
        if os.path.exists(settingsFileCheck):
            return True
    else:
        return False
#
	
def ParseOltData(FoundAddon):
    AddonININame = FoundAddon  + '.ini'   
    Addoninipath  = os.path.join(inipath, AddonININame)
    response = GrabSettingsFromOlt(FoundAddon)
    result   = response['result'] 
    ChannelsResult = result['files']    
    ExtrasFileToWrite  = file(Addoninipath, 'w')  
    ExtrasFileToWrite.write('[')
    ExtrasFileToWrite.write(FoundAddon)
    ExtrasFileToWrite.write(']')
    ExtrasFileToWrite.write('\n')   
    TheAddonURL = []   
    for channel in ChannelsResult:
        ParsedChannels = channel['label']
        stream  = channel['file']
        ChannelURL  = GetOltStuff(FoundAddon, ParsedChannels)
        channel = RemoveOltChanCrap(FoundAddon, ChannelURL)
        FinalChannelString = channel + '\t\t=' + stream#Jules: make correct formating for channel names
        TheAddonURL.append(FinalChannelString)
        TheAddonURL.sort()
    for item in TheAddonURL:
      ExtrasFileToWrite.write("%s\n" % item)
    ExtrasFileToWrite.close()
    Clean_Names_Olt(Addoninipath,tmp_File)
#
def GrabSettingsFromOlt(FoundAddon):
    Addon    =  xbmcaddon.Addon(FoundAddon)
    username =  Addon.getSetting('Username')
    password =  Addon.getSetting('Password')
    BeginningOfPluginString   = 'plugin://' + FoundAddon    
    urlBody= '/?action=stream_video&extra&page&plot&thumbnail=&title=All&url='
    endOfString    =  GetOltVariables(FoundAddon)
    startOfString  =  BeginningOfPluginString + urlBody + endOfString
    GrabThisUrl = 'username=' + username + '&password=' + password + '&type=get_live_streams&cat_id=0'
    queryURL = BeginningOfPluginString  + '/?action=security_check&extra&page&plot&thumbnail&title=Live%20TV&url'
    query = startOfString +  urllib.quote_plus(GrabThisUrl)
    checkthisurl = ('{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"%s"}, "id": 1}' % queryURL)
    checkthisurltoo = ('{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"%s"}, "id": 1}' % query)   
    try:
        xbmc.executeJSONRPC(checkthisurl)
        response = xbmc.executeJSONRPC(checkthisurltoo)
        content = json.loads(response.decode('utf-8', 'ignore'))
        return content
    except Exception as e:
        #RunSetSetting(e)
        print e
        return {'Error' : 'Plugin Error'}
#    
def GetOltStuff(FoundAddon, RemoveURLGarbage):
    RemoveURLGarbage = RemoveURLGarbage.replace('COLOR+', '').replace(' [/B]', '').replace('[COLOR white]', '').replace('[/COLOR]', '').replace('[COLOR white]', '').replace('COLOR+steelblue', '')      
    return RemoveURLGarbage
#    
def RemoveOltChanCrap(FoundAddon, FoundChannels):
    channel = FoundChannels.rsplit('[/B]', 1)[0].split('[B]', 1)[-1]        
    return channel
#       
def GetOltVariables(FoundAddon):
    Addon    =  xbmcaddon.Addon(FoundAddon) 
    addre_ss =  'http://onestream.ddns.net' 
    po_rt =  '5454'
    correct_address = addre_ss + ':' + po_rt + '/enigma2.php?'
    return correct_address
	

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
def Clean_Names_Olt(Clean_Name,tmpFile):
    if os.path.exists(tmpFile):
        os.remove(tmpFile)
    os.rename(Clean_Name, tmpFile)
    s=open(tmpFile).read()

                     
    s=s.replace('BBC 1','BBC One')
    s=s.replace('BBC 2','BBC Two')
    s=s.replace('BBC 4','BBC FOUR')
    s=s.replace('ITV 1','ITV1')
    s=s.replace('ITV 2','ITV2')
    s=s.replace('ITV 3','ITV3')
    s=s.replace('ITV 4','ITV4')
    s=s.replace('SKY ONE','Sky1')
    s=s.replace('.ts','.m3u8')



    f=open(Clean_Name,'a')
    f.write(s)
    f.close()
    os.remove(tmpFile)
    return

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