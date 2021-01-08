#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla              *
*             skin by MMark            *
*             01/12/2020               *
****************************************
'''
#Info http://t.me/tivustream
# from __future__ import print_function
from . import _
from Components.Label import Label
from Components.ConfigList import ConfigListScreen, ConfigList
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import *
import os
import re
import glob
from enigma import getDesktop
from enigma import addFont
from enigma import eTimer
from enigma import loadPNG
from skin import loadSkin
from os import path, listdir, remove, mkdir, chmod, sys
from Tools.Directories import fileExists, pathExists
global isDreamOS, new_bouquet, SKIN_PATH, HD

Version        = '1.4'
plugin_path    = os.path.dirname(sys.modules[__name__].__file__)
DESKHEIGHT     = getDesktop(0).size().height()
HD             = getDesktop(0).size()
SKIN_PATH      = plugin_path
iconpic        = plugin_path+ '/plugin.png'
tmp_bouquet    = plugin_path + '/tmp'
new_bouquet    = tmp_bouquet + '/bouquets.tv'

#================
isDreamOS = False
try:
    from enigma import eMediaDatabase
    isDreamOS = True
except:
    isDreamOS = False

# SCREEN PATH SETTING
if HD.width() > 1280:
    if isDreamOS:
        SKIN_PATH = plugin_path + '/Skin/fhd/dreamOs'
    else:
        SKIN_PATH = plugin_path + '/Skin/fhd'
else:
    if isDreamOS:
        SKIN_PATH = plugin_path + '/Skin/hd/dreamOs'
    else:
        SKIN_PATH = plugin_path + '/Skin/hd'

def add_skin_font():
    font_path = plugin_path + '/fonts/'
    addFont(font_path + 'Roboto.ttf', 'cvfont', 100, 1)

class MenuListSelect(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if HD.width() > 1280:
            self.l.setFont(0, gFont('Regular', 34))
            self.l.setItemHeight(50)
        else:
            self.l.setFont(0, gFont('Regular', 22))
            self.l.setItemHeight(45)

def lista_bouquet():
    iptv_list = []
    f = open(new_bouquet, 'w')
    f.write('NAME Bouquets (TV)\n')
    for iptv_file in sorted(glob.glob('/etc/enigma2/userbouquet.*.tv')):
        usbq = open(iptv_file, 'r').read()
        usbq_lines = usbq.strip().lower()
        if 'http' in usbq_lines:
            iptv_list.append(os.path.basename(iptv_file))
            strep_bq = iptv_file.replace('/etc/enigma2/','')
            f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(strep_bq) + '" ORDER BY bouquet' +'\n')
            print('iptv_file ', iptv_file)
            os.system('cp -rf /etc/enigma2/'+ str(strep_bq) + ' ' + tmp_bouquet )
    for iptv_file in sorted(glob.glob('/etc/enigma2/subbouquet.*.tv')):
        usbq = open(iptv_file, 'r').read()
        usbq_lines = usbq.strip().lower()
        if 'http' in usbq_lines:
            iptv_list.append(os.path.basename(iptv_file))
            strep_bq = iptv_file.replace('/etc/enigma2/','')
            f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(strep_bq) + '" ORDER BY bouquet' +'\n')
            print('iptv_file 2 ', iptv_file)
            os.system('cp -rf /etc/enigma2/'+ str(strep_bq)  + ' ' + tmp_bouquet )
    f.close()
    if not iptv_list:
        return False
    else:
        return iptv_list

def clear_bqt():
    if fileExists(new_bouquet):
        path = tmp_bouquet
        try:
            cmd = 'rm -f %s/*.tv' % path
            os.system(cmd)
            cmd2 = 'rm -f %s' %new_bouquet
            os.system(cmd2)
        except Exception as ex:
            print(ex)
            print('delete ')

class ListSelect:

    def __init__(self):
        pass

    def ReadMemList(self):
            pass

    def readBouquetsList(self, pwd, bouquetname):
        try:
            f = open(pwd + '/' + bouquetname)
        except Exception as e:
            print(e)
            return
        ret = []
        while True:
            line = f.readline()
            if line == '':
                break
            if line[:8] != '#SERVICE':
                continue
            tmp = line.strip().split(':')
            line = tmp[len(tmp) - 1]
            filename = None
            if line[:12] == 'FROM BOUQUET':
                tmp = line[13:].split(' ')
                filename = tmp[0].strip('"')
            else:
                filename = line
            if filename:
                    try:
                        fb = open(pwd + '/' + filename)
                    except Exception as e:
                        continue
                    tmp = fb.readline().strip()
                    print('tmp 1 :', tmp)

                    s1=fb.readline().strip()
                    items = []
                    item = tmp + "###" + s1
                    items.append(item)
                    # items.sort()
                    for item in items:
                        if not 'http' in item:
                            continue
                        tmp = item.split("###")[0]
                        s1 = item.split("###")[1]
                        print('tmp2: ', tmp)
                        print('s2: ', s1)
                    ########
                    if tmp[:6] == '#NAME ':
                        ret.append([filename, tmp[6:]])
                    else:
                        ret.append([filename, filename])
                    fb.close()
        return ret


    def ReadBouquet(self, pwd):
        return self.readBouquetsList(pwd, 'bouquets.tv')

    def TvList(self):
        jload = self.ReadMemList()
        self.bouquetlist = []
        for x in self.ReadBouquet(tmp_bouquet):
            value = '0'
            try:
                for j, jx in jload:
                    if j == x[0] and jx.find(x[1]) != -1:
                            value = '1'
                            break
            except:
                pass
            self.bouquetlist.append((x[0], x[1], value))
        return self.bouquetlist

class TvToM3uPanel(Screen):

    def __init__(self, session):
        self.session = session
        skin = SKIN_PATH + '/TvToM3uPanel.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.ListSelect = ListSelect()
        self['text'] = Label(_('Select List IPTV and convert to M3U in /tmp\nby Lululla\n\n     www.corvoboys.com'))
        self['version'] = Label(_('Version %s' % Version))
        self['Key_Green'] = Label(_('Convert') + ' IPTV /tmp/tvtom3u' )
        self['Key_Yellow'] = Label(_('Backup') + ' IPTV /tmp/tvtom3u')
        self['Key_Blue'] = Label(' ')
        self['Key_Red'] = Label(_('Exit'))
        self['MENU'] = MenuListSelect([])
        self['MENU'].selectionEnabled(1)
        lista_bouquet()
        self.Menu()
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'SetupActions'], {'ok': self.keyGreen,
         'cancel': self.Uscita,
         'green': self.keyGreen,
         'yellow': self.keyYellow,
         'blue': self.Uscita,
         'red': self.Uscita}, -1)

    def Uscita(self):
        clear_bqt()
        self.close()

    def hauptListEntry(self, dir, name, value):
        res = [(dir, name, value)]
        icon = '/usr/lib/enigma2/python/Plugins/Extensions/TvToM3uPanel/Skin/redpanel.png'
        if value == '1':
            icon = '/usr/lib/enigma2/python/Plugins/Extensions/TvToM3uPanel/Skin/greenpanel.png'
        try:
            name = name.split('   ')[0]
        except:
            pass

        if HD.width() > 1280:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 15), size=(20, 20), png=loadPNG(icon))) #png=loadPic(icon, 20, 20, 0, 0, 0, 1)))
            res.append(MultiContentEntryText(pos=(50, 7), size=(425, 40), font=0, text=name, flags=RT_HALIGN_LEFT))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=dir, flags=RT_HALIGN_LEFT))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=value, flags=RT_HALIGN_LEFT))
        else:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 11), size=(20, 20), png=loadPNG(icon))) #png=loadPic(icon, 20, 20, 0, 0, 0, 1)))
            res.append(MultiContentEntryText(pos=(50, 7), size=(425, 40), font=0, text=name, flags=RT_HALIGN_LEFT))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=dir, flags=RT_HALIGN_LEFT))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=value, flags=RT_HALIGN_LEFT))
        return res


    def Menu(self):
        self.jA = []
        for dir, name, value in self.ListSelect.TvList():
                self.jA.append(self.hauptListEntry(dir, name, value))
        self['MENU'].setList(self.jA)
    '''
    def OkSelect(self):
        NewName = self['MENU'].getCurrent()[0][1]
        NewDir = self['MENU'].getCurrent()[0][0]
        self.list = []
        for dir, name, value in self.ListSelect.TvList():
            if dir == NewDir and name == NewName:
                if value == '0':
                    self.list.append((dir, name, '1'))
            elif value == '1':
                self.list.append((dir, name, '1'))

        self.Menu()
        self['MENU'].selectionEnabled(1)
    '''
    def keyGreen(self):
        url = self['MENU'].getCurrent()[0][1]
        if url == -1 or None:
            return
        else:
            try:
                for dir, name, value in self.ListSelect.TvList():
                    if url == name : 
                        '''
                        # problem or url in name ? ?      or if not name.find(url) != -1:
                        '''
                        print('dir : ', dir)
                        print('name: ', name)
                        print('value: ', value)
                        url = tmp_bouquet +'/%s' % dir
                        print('url folder =', url)
                        f = open(url, 'r')
                        content = f.read()
                        print('In content =', content)
                        # regexcat = '#SERVICE.*?:http(.*?)\\n#DESCRIPTION(.*?)\\n'
                        regexcat = '#SERVICE.*?0:(.*?)\\n#DESCRIPTION(.*?)\\n'
                        match = re.compile(regexcat, re.DOTALL).findall(content)
                        print('In match =', match)
                        nameM3u = name.replace(' ', '') # for FILE_M3U
                        nameM3u = nameM3u.lower()
                        print('In nameM3u =', nameM3u)
                        FILE_M3U = '/tmp/tvtom3u/%s.m3u' % nameM3u
                        WriteBouquet = open(FILE_M3U, 'w')
                        WriteBouquet.write('#EXTM3U\n')

                        for url, name in match:
                                    try:
                                        """
                                        n1 = url.find(":",0)
                                        url = url[:n1]
                                        url= url.replace('%3a',':')
                                        url= 'http' + url
                                        """
                                        # url= 'http' + url
                                        n1 = url.find("http",0)
                                        if n1>-1:
                                               url = url[n1:]
                                               url= url.replace('%3a',':')
                                        else:
                                               n1 = url.find("rtmp",0)
                                               url = url[n1:]
                                               url= url.replace('%3a',':')
                                        n2 = url.rfind(":",0)
                                        url = url[:n2]
                                        print('url: ', url)
                                        print('namex: ', name)
                                    except:
                                        pass
                                        pass
                                    WriteBouquet.write('#EXTINF:-1 tvg-ID="" tvg-name="%s" tvg-logo="" group-title="",%s\n' %(name,name) )
                                    print('rep1-url:', url)
                                    WriteBouquet.write('%s\n' % url)

                        f.close()
                        WriteBouquet.close()
                self.mbox = self.session.open(MessageBox, _('Export Succes'), MessageBox.TYPE_INFO, timeout=8)

            except:
                print('++++++++++ERROR CONVERT+++++++++++++')

    def keyYellow(self):
        iptv_to_save = lista_bouquet()
        if iptv_to_save:
            for iptv in iptv_to_save:
                os.system('cp -rf '+ tmp_bouquet + '/' + iptv + ' ' + '/var/volatile/tmp/tvtom3u/' + iptv)
        self.mbox = self.session.open(MessageBox, _('Command Send - Check'), MessageBox.TYPE_INFO, timeout=8)


def Main(session, **kwargs):
    add_skin_font()
    if not os.path.exists('/var/volatile/tmp/tvtom3u/'):
        try:
            os.makedirs('/var/volatile/tmp/tvtom3u/')
        except OSError as e:
            print ('Error creating directory tvtom3u')
    session.open(TvToM3uPanel)

def Plugins(**kwargs):
    return [PluginDescriptor(name='TvToM3u', description='Enigma2 Iptv Converter Bouquet', icon= plugin_path + '/plugin.png', where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=Main)]
