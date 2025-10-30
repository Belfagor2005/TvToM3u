#!/usr/bin/python
# -*- coding: utf-8 -*-

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext
import os

PluginLanguageDomain = 'TvToM3uPanel'
PluginLanguagePath = 'Extensions/TvToM3uPanel/locale'

isDreamOS = False
if os.path.exists("/var/lib/dpkg/status"):
    isDreamOS = True


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
    if isDreamOS:  # check if opendreambox image
        # getLanguage returns e.g. "fi_FI" for "language_country"
        lang = language.getLanguage()[:2]
        # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs
        # it!
        os.environ["LANGUAGE"] = lang
    gettext.bindtextdomain(
        PluginLanguageDomain,
        resolveFilename(
            SCOPE_PLUGINS,
            PluginLanguagePath))


if isDreamOS:  # check if DreamOS image
    def _(txt): return gettext.dgettext(
        PluginLanguageDomain, txt) if txt else ""
else:
    def _(txt):
        if gettext.dgettext(PluginLanguageDomain, txt):
            return gettext.dgettext(PluginLanguageDomain, txt)
        else:
            print(("[%s] fallback to default translation for %s" %
                  (PluginLanguageDomain, txt)))
            return gettext.gettext(txt)
localeInit()
language.addCallback(localeInit)
