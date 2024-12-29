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
from Components.MultiContent import (MultiContentEntryText, MultiContentEntryPixmapAlphaTest)
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import fileExists
from enigma import (
    addFont,
    RT_HALIGN_LEFT,
    RT_VALIGN_CENTER,
    getDesktop,
    loadPNG,
    gFont,
    eListboxPythonMultiContent,
)
from os import (path, sys)
from os.path import exists as file_exists
import codecs
import glob
import os
import re

try:
    from urllib import unquote, quote  # Python 2
except ImportError:
    from urllib.parse import unquote, quote  # Python 3


global downloadfree

Version = '2.0'
title_plug = '..:: Enigma2 M3U Converter Bouquet V. %s ::..' % Version
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
res_plugin_path = plugin_path + '/Skin/'
iconpic = plugin_path + '/plugin.png'
tmp_bouquet = plugin_path + '/tmp'
new_bouquet = tmp_bouquet + '/bouquets.tv'
downloadfree = "/tmp/tvtom3u/"
screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    skin_m3up = plugin_path + '/Skin/uhd/'
elif screenwidth.width() == 1920:
    skin_m3up = plugin_path + '/Skin/fhd/'
else:
    skin_m3up = plugin_path + '/Skin/hd/'
if os.path.exists('/var/lib/dpkg/info'):
    skin_m3up = skin_m3up + '/dreamOs/'


def add_skin_font():
    font_path = plugin_path + '/fonts/'
    addFont(font_path + 'Roboto.ttf', 'cvfont', 100, 1)


if not os.path.exists('/tmp/tvtom3u/'):
    try:
        os.makedirs('/tmp/tvtom3u/')
    except OSError as e:
        print('Error creating directory tvtom3u', e)

try:
    from Components.UsageConfig import defaultMoviePath
    downloadfree = defaultMoviePath()
except:
    if os.path.exists("/usr/bin/apt-get"):
        downloadfree = ('/media/hdd/movie/')


def get_safe_filename(filename, fallback=''):
    '''Convert filename to safe filename'''
    import unicodedata
    import six
    name = filename.replace(' ', '_').replace('/', '_')
    if isinstance(name, six.text_type):
        name = name.encode('utf-8')
    name = unicodedata.normalize('NFKD', six.text_type(name, 'utf_8', errors='ignore')).encode('ASCII', 'ignore')
    name = re.sub(b'[^a-z0-9-_]', b'', name.lower())
    if not name:
        name = fallback
    return six.ensure_str(name)


def parse_m3u(file_path):
    channels = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                info = lines[i].strip()
                url = lines[i + 1].strip()
                if info.startswith('#EXTINF:'):
                    match = re.search(r'tvg-name="([^"]*)".*,(.*)$', info)
                    if match:
                        name = match.group(2)
                        channels.append((name, url))
    return channels


def write_tv(channels, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for name, url in channels:
            decoded_name = unquote(name)
            file.write(f'{decoded_name} {url}\n')


def parse_tv(file_path):
    channels = []
    with codecs.open(file_path, "r", encoding="utf-8") as file:
        line = file.read()
        regexcat = '#SERVICE.*?(.*?)\\n#DESCRIPTION (.*?)\\n'
        match = re.compile(regexcat).findall(line)
        for url, name in match:
            n1 = url.find("http", 0)
            if n1 > - 1:
                url = url[n1:]
                url = url.replace('%3a', ':')
                channels.append((name, url))                
    return channels


def write_m3u(channels, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('#EXTM3U\n')
        for name, url in channels:
            encoded_name = quote(name)
            file.write(f'#EXTINF:-1 tvg-name="{encoded_name}",{name}\n')
            file.write(f'{url}\n')


def filter_channels(channels, keyword):
    return [channel for channel in channels if keyword.lower() in channel[0].lower()]


def sort_channels(channels):
    return sorted(channels, key=lambda x: x[0].lower())


def remove_duplicates(channels):
    seen = set()
    return [channel for channel in channels if not (channel[0] in seen or seen.add(channel[0]))]


def print_channel_list(channels):
    for i, (name, url) in enumerate(channels, 1):
        print(f"{i}. {name}")


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
        usbq = open(iptv_file, 'r', encoding="latin-1").read()
        usbq_lines = usbq.strip().lower()
        if 'http' in usbq_lines.strip().lower():
            if iptv_file not in iptv_list:
                iptv_list.append(os.path.basename(iptv_file))
                strep_bq = iptv_file.replace('/etc/enigma2/', '')
                f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(strep_bq) + '" ORDER BY bouquet' + '\n')
                os.system('cp -rf /etc/enigma2/' + str(strep_bq) + ' ' + tmp_bouquet)
    for iptv_file in sorted(glob.glob('/etc/enigma2/subbouquet.*.tv')):
        usbq = open(iptv_file, 'r', encoding="latin-1").read()
        usbq_lines = usbq.strip().lower()
        if 'http' in usbq_lines.strip().lower():
            if iptv_file not in iptv_list:
                iptv_list.append(os.path.basename(iptv_file))
                strep_bq = iptv_file.replace('/etc/enigma2/', '')
                f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(strep_bq) + '" ORDER BY bouquet' + '\n')
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

    def openVi(self, file):
        from .type_utils import zEditor
        if fileExists(file):
            self.session.open(zEditor, file)

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
        if screenwidth.width() == 2560:  # 1770
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 15), size=(24, 24), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(60, 0), size=(1500, 54), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
        elif screenwidth.width() == 1920:  # 1335
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(24, 24), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
        else:  # 890
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 9), size=(24, 24), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(60, 0), size=(800, 40), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
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
        if url == -1 or None:
            return
        else:
            for dir, name, value in self.ListSelect.TvList():
                if url == name:
                    WriteBouquet = ''
                    url = tmp_bouquet + '/%s' % dir
                    nameM3u = get_safe_filename(name).replace(' ', '').lower()
                    FILE_M3U = '%s%s.m3u' % (downloadfree, nameM3u)
                    channels = parse_tv(url)
                    write_m3u(channels, FILE_M3U)
                    print("Conversione da TV a M3U completata.")
            self.session.open(MessageBox, _('Export Succes'), MessageBox.TYPE_INFO, timeout=8)
            self.openVi(FILE_M3U)

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
