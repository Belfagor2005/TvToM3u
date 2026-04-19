#!/usr/bin/python
# -*- coding: utf-8 -*-

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext
import sys
import os
from os.path import dirname

__version__ = "2.1"
title_plug = '..:: Enigma2 M3U Converter Bouquet V. %s ::..' % __version__
plugin_path = dirname(sys.modules[__name__].__file__)
res_plugin_path = plugin_path + '/Skin/'
iconpic = plugin_path + '/plugin.png'
tmp_bouquet = plugin_path + '/tmp'
new_bouquet = tmp_bouquet + '/bouquets.tv'

PluginLanguageDomain = 'TvToM3u'
PluginLanguagePath = 'Extensions/TvToM3u/locale'


def paypal():
    conthelp = "If you like what I do you\n"
    conthelp += "can contribute with a coffee\n"
    conthelp += "scan the qr code and donate € 1.00"
    return conthelp


def wanStatus():
    publicIp = ''
    try:
        file = os.popen('wget -qO - ifconfig.me')
        public = file.read()
        publicIp = "Wan %s" % (str(public))
    except BaseException:
        if os.path.exists("/tmp/currentip"):
            os.remove("/tmp/currentip")
    return publicIp


def localeInit():
    gettext.bindtextdomain(
        PluginLanguageDomain,
        resolveFilename(
            SCOPE_PLUGINS,
            PluginLanguagePath))


def _(txt):
    if gettext.dgettext(PluginLanguageDomain, txt):
        return gettext.dgettext(PluginLanguageDomain, txt)
    else:
        print(("[%s] fallback to default translation for %s" %
              (PluginLanguageDomain, txt)))
        return gettext.gettext(txt)


localeInit()
language.addCallback(localeInit)
