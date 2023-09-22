#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla              *
*             skin by MMark            *
*             01/09/2023               *
****************************************
Info http://t.me/tivustream
'''
from __future__ import print_function
from . import _, paypal
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.MultiContent import MultiContentEntryPixmapAlphaTest
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from enigma import addFont
from enigma import RT_HALIGN_LEFT, RT_VALIGN_CENTER
from enigma import getDesktop
from enigma import loadPNG, gFont
from enigma import eListboxPythonMultiContent
from os import path, sys
from os.path import exists as file_exists
import codecs
import glob
import os
import re
global new_bouquet, skin_m3up, downloadfree

Version = '1.8'
title_plug = '..:: Enigma2 M3U Converter Bouquet V. %s ::..' % Version
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
res_plugin_path = plugin_path + '/Skin/'
iconpic = plugin_path + '/plugin.png'
tmp_bouquet = plugin_path + '/tmp'
new_bouquet = tmp_bouquet + '/bouquets.tv'
downloadfree = "/tmp/tvtom3u/"
skin_m3up = os.path.join(res_plugin_path, "hd/")
screenwidth = getDesktop(0).size()
if screenwidth.width() == 1920:
    skin_m3up = res_plugin_path + 'fhd/'
if screenwidth.width() == 2560:
    skin_m3up = res_plugin_path + 'uhd/'
if os.path.exists('/var/lib/dpkg/info'):
    skin_m3up = skin_m3up + 'dreamOs/'


def add_skin_font():
    font_path = plugin_path + '/fonts/'
    addFont(font_path + 'Roboto.ttf', 'cvfont', 100, 1)


if not os.path.exists('/tmp/tvtom3u/'):
    try:
        os.makedirs('/tmp/tvtom3u/')
    except OSError as e:
        print ('Error creating directory tvtom3u')

downloadfree = '/tmp/'
try:
    from Components.UsageConfig import defaultMoviePath
    downloadfree = defaultMoviePath()
except:
    if os.path.exists("/usr/bin/apt-get"):
        downloadfree = ('/media/hdd/movie/')


class MenuListSelect(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)

        if screenwidth.width() == 2560:
            self.l.setFont(0, gFont('Regular', 48))
            self.l.setItemHeight(56)
        elif screenwidth.width() == 1920:
            self.l.setFont(0, gFont('Regular', 30))
            self.l.setItemHeight(50)
        else:
            self.l.setFont(0, gFont('Regular', 24))
            self.l.setItemHeight(45)


def lista_bouquet():
    iptv_list = []
    f = ''
    if sys.version_info[0] == 3:
        f = open(new_bouquet, 'w', encoding='UTF-8')
    else:
        f = open(new_bouquet, 'w')
    f.write('NAME Bouquets (TV)\n')
    for iptv_file in sorted(glob.glob('/etc/enigma2/userbouquet.*.tv')):
        usbq = open(iptv_file, 'r').read()
        usbq_lines = usbq.strip().lower()
        if 'http' in usbq_lines:
            iptv_list.append(os.path.basename(iptv_file))
            strep_bq = iptv_file.replace('/etc/enigma2/', '')
            f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(strep_bq) + '" ORDER BY bouquet' + '\n')
            # print('iptv_file ', iptv_file)
            os.system('cp -rf /etc/enigma2/' + str(strep_bq) + ' ' + tmp_bouquet)

    for iptv_file in sorted(glob.glob('/etc/enigma2/subbouquet.*.tv')):
        usbq = open(iptv_file, 'r').read()
        usbq_lines = usbq.strip().lower()
        if 'http' in usbq_lines:
            iptv_list.append(os.path.basename(iptv_file))
            strep_bq = iptv_file.replace('/etc/enigma2/', '')
            f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(strep_bq) + '" ORDER BY bouquet' + '\n')
            # print('iptv_file 2 ', iptv_file)
            os.system('cp -rf /etc/enigma2/' + str(strep_bq) + ' ' + tmp_bouquet)
    f.close()
    if len(iptv_list) < 0:
        return False
    else:
        return iptv_list


def clear_bqt():
    if file_exists(new_bouquet):
        try:
            cmd = 'rm -f %s/*.tv' % path
            os.system(cmd)
            cmd2 = 'rm -f %s' % new_bouquet
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
                    print(str(e))
                    continue
                tmp = fb.readline().strip()
                # print('tmp 1 :', tmp)
                s1 = fb.readline().strip()
                items = []
                item = tmp + "###" + s1
                items.append(item)
                # items.sort()
                for item in items:
                    if 'http' not in item:
                        continue
                    tmp = item.split("###")[0]
                    s1 = item.split("###")[1]
                    # print('tmp2: ', tmp)
                    # print('s1: ', s1)
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


class TvToM3u(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_m3up, 'TvToM3uPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = title_plug
        self.ListSelect = ListSelect()
        self['text'] = Label(_('Select IPTV List and convert to M3U in\n%s') % downloadfree)
        self['version'] = Label(_('Version %s by Lululla' % Version))
        self['Key_Green'] = Label(_('Convert') + ' IPTV %s' % downloadfree)
        self['Key_Yellow'] = Label(_('Backup') + ' IPTV %s' % downloadfree)
        # self['Key_Blue'] = Label(' ')
        self['Key_Red'] = Label(_('Exit'))
        self["paypal"] = Label()
        self['MENU'] = MenuListSelect([])
        self['MENU'].selectionEnabled(1)
        lista_bouquet()
        self.Menu()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.keyGreen,
                                                       'cancel': self.Uscita,
                                                       'green': self.keyGreen,
                                                       'yellow': self.keyYellow,
                                                       # 'blue': self.Uscita,
                                                       'red': self.Uscita}, -1)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        payp = paypal()
        self["paypal"].setText(payp)
        self.setTitle(self.setup_title)

    def Uscita(self):
        clear_bqt()
        self.close()

    def hauptListEntry(self, dir, name, value):
        res = [(dir, name, value)]
        icon = '%sredpanel.png' % res_plugin_path
        if value == '1':
            icon = '%sgreenpanel.png' % res_plugin_path
        try:
            name = name.split('   ')[0]
        except:
            pass
        if screenwidth.width() == 2560:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 15), size=(24, 24), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(60, 0), size=(700, 54), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=dir, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=value, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))

        elif screenwidth.width() == 1920:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(24, 24), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(60, 0), size=(800, 50), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=dir, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=value, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
        else:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 9), size=(24, 24), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(60, 0), size=(400, 40), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=dir, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=value, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
        return res

    def Menu(self):
        self.jA = []
        for dir, name, value in self.ListSelect.TvList():
            self.jA.append(self.hauptListEntry(dir, name, value))
        self['MENU'].setList(self.jA)

    def keyGreen(self):
        url = self['MENU'].getCurrent()[0][1]
        # print('ok green', url)
        if url == -1 or None:
            return
        else:
            try:
                for dir, name, value in self.ListSelect.TvList():
                    if url == name:
                        WriteBouquet = ''
                        url = tmp_bouquet + '/%s' % dir
                        with codecs.open(url, "r", encoding="utf-8") as f:
                            content = f.read()
                        # f = open(url, 'r')
                        # content = f.read()
                        regexcat = '#SERVICE.*?(.*?)\\n#DESCRIPTION (.*?)\\n'
                        match = re.compile(regexcat).findall(content)
                        nameM3u = name.replace(' ', '').lower()
                        FILE_M3U = '%s/%s.m3u' % (downloadfree, nameM3u)
                        if sys.version_info[0] == 3:
                            WriteBouquet = open(FILE_M3U, 'w', encoding='UTF-8')
                        else:
                            WriteBouquet = open(FILE_M3U, 'w')
                        WriteBouquet.write('#EXTM3U\n')
                        for url, name in match:
                            n1 = url.find("http", 0)
                            if n1 > - 1:
                                url = url[n1:]
                                url = url.replace('%3a', ':')
                                WriteBouquet.write('#EXTINF:-1 tvg-ID="" tvg-name="%s" tvg-logo="" group-title="",%s\n' % (name, name))
                            n3 = url.find("rtmp", 0)
                            if n3 > - 1:
                                url = url[n3:]
                                url = url.replace('%3a', ':')
                                WriteBouquet.write('#EXTINF:-1 tvg-ID="" tvg-name="%s" tvg-logo="" group-title="",%s\n' % (name, name))
                            WriteBouquet.write('%s\n' % url)
                        f.close()
                        WriteBouquet.close()
                self.session.open(MessageBox, _('Export Succes'), MessageBox.TYPE_INFO, timeout=8)
            except:
                print('++++++++++ERROR CONVERT+++++++++++++')

    def keyYellow(self):
        iptv_to_save = lista_bouquet()
        if iptv_to_save:
            for iptv in iptv_to_save:
                os.system('cp -rf ' + tmp_bouquet + '/' + iptv + ' ' + '/tmp/tvtom3u/' + iptv)
        self.mbox = self.session.open(MessageBox, _('Command Save Send - Check'), MessageBox.TYPE_INFO, timeout=8)


def Main(session, **kwargs):
    add_skin_font()
    session.open(TvToM3u)


def Plugins(**kwargs):
    return [PluginDescriptor(name='TvToM3u', description=title_plug, icon=iconpic, where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=Main)]
