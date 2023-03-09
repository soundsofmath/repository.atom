import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import glob
import os
import re
try:  # Python 3
    from urllib.parse import quote_plus
    from urllib.request import urlretrieve
except ImportError:  # Python 2
    from urllib import quote_plus
    from urllib import urlretrieve
from resources.libs.common import directory
from resources.libs.common.config import CONFIG


def trakt_menu():
    from resources.libs import traktit

    for trakt in traktit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(traktit.TRAKTID[trakt]['plugin'])):
            name = traktit.TRAKTID[trakt]['name']
            path = traktit.TRAKTID[trakt]['path']
            saved = traktit.TRAKTID[trakt]['saved']
            file = traktit.TRAKTID[trakt]['file']
            user = CONFIG.get_setting(saved)
            auser = traktit.trakt_user(trakt)
            icon = traktit.TRAKTID[trakt]['icon'] if os.path.exists(path) else CONFIG.ICONTRAKT
            fanart = traktit.TRAKTID[trakt]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Trakt', trakt)
            menu2 = create_save_data_menu('Trakt', trakt)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=trakt)'.format(CONFIG.ADDON_ID, trakt)))

            directory.add_file('{0}'.format(name), icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
            if not os.path.exists(path):
                directory.add_file('[COLOR red]Addon Data: Not Installed[/COLOR]', icon=icon, fanart=fanart, menu=menu)
            elif not auser:
                directory.add_file('[COLOR red]Addon Data: Not Registered[/COLOR]', {'mode': 'authtrakt', 'name': trakt}, icon=icon, fanart=fanart, menu=menu)
            else:
                directory.add_file('[COLOR springgreen]Addon Data: {0}[/COLOR]'.format(auser), {'mode': 'authtrakt', 'name': trakt}, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file):
                    directory.add_file('[COLOR springgreen]Trakt Data Saved![/COLOR]', icon=icon, fanart=fanart)
                else:
                    directory.add_file('[COLOR red]Trakt Data Not Saved![/COLOR]', icon=icon, fanart=fanart)
            else:
                directory.add_file('[COLOR springgreen]Saved Data: {0}[/COLOR]'.format(user), icon=icon, fanart=fanart, menu=menu2)

    directory.add_separator(icon=icon, themeit=CONFIG.THEME3)
    directory.add_file('Save All Trakt Data', {'mode': 'savetrakt', 'name': 'all'}, icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    directory.add_file('Recover All Saved Trakt Data', {'mode': 'restoretrakt', 'name': 'all'}, icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    directory.add_file('Clear All Addon Trakt Data', {'mode': 'addontrakt', 'name': 'all'}, icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    directory.add_file('Clear All Saved Trakt Data', {'mode': 'cleartrakt', 'name': 'all'}, icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)


def debrid_menu():
    from resources.libs import debridit

    for debrid in debridit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(debridit.DEBRIDID[debrid]['plugin'])):
            name = debridit.DEBRIDID[debrid]['name']
            path = debridit.DEBRIDID[debrid]['path']
            saved = debridit.DEBRIDID[debrid]['saved']
            file = debridit.DEBRIDID[debrid]['file']
            user = CONFIG.get_setting(saved)
            auser = debridit.debrid_user(debrid)
            icon = debridit.DEBRIDID[debrid]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = debridit.DEBRIDID[debrid]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Debrid', debrid)
            menu2 = create_save_data_menu('Debrid', debrid)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=debrid)'.format(CONFIG.ADDON_ID, debrid)))

            directory.add_file('{0}'.format(name), icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
            if not os.path.exists(path):
                directory.add_file('[COLOR red]Addon Data: Not Installed[/COLOR]', icon=icon, fanart=fanart, menu=menu)
            elif not auser:
                directory.add_file('[COLOR red]Addon Data: Not Registered[/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, fanart=fanart, menu=menu)
            else:
                directory.add_file('[COLOR springgreen]Addon Data: {0}[/COLOR]'.format(auser), {'mode': 'authdebrid', 'name': debrid}, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file):
                    directory.add_file('[COLOR springgreen]Debrid Data Saved![/COLOR]', icon=icon, fanart=fanart)
                else:
                    directory.add_file('[COLOR red]Debrid Data Not Saved![/COLOR]', icon=icon, fanart=fanart)
            else:
                directory.add_file('[COLOR springgreen]Saved Data: {0}[/COLOR]'.format(user), icon=icon, fanart=fanart, menu=menu2)

    directory.add_separator(icon=icon, themeit=CONFIG.THEME3)
    directory.add_file('Save All Debrid Data', {'mode': 'savedebrid', 'name': 'all'}, icon=CONFIG.ICONDEBRID, themeit=CONFIG.THEME3)
    directory.add_file('Recover All Saved Debrid Data', {'mode': 'restoredebrid', 'name': 'all'}, icon=CONFIG.ICONDEBRID, themeit=CONFIG.THEME3)
    directory.add_file('Clear All Addon Debrid Data', {'mode': 'addondebrid', 'name': 'all'}, icon=CONFIG.ICONDEBRID, themeit=CONFIG.THEME3)
    directory.add_file('Clear All Saved Debrid Data', {'mode': 'cleardebrid', 'name': 'all'}, icon=CONFIG.ICONDEBRID, themeit=CONFIG.THEME3)


def create_addon_data_menu(add='', name=''):
    menu_items = []

    add2 = quote_plus(add.lower().replace(' ', ''))
    add3 = add.replace('Debrid', 'Real Debrid')
    name2 = quote_plus(name.lower().replace(' ', ''))
    name = name.replace('url', 'URL Resolver')
    menu_items.append((CONFIG.THEME2.format(name.title()), ' '))
    menu_items.append((CONFIG.THEME3.format('Save {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=save{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Restore {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=restore{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Clear {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=clear{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))

    menu_items.append((CONFIG.THEME2.format('{0} Settings'.format(CONFIG.ADDONTITLE)), 'RunPlugin(plugin://{0}/?mode=settings)'.format(CONFIG.ADDON_ID)))

    return menu_items


def create_save_data_menu(add='', name=''):
    menu_items = []

    add2 = quote_plus(add.lower().replace(' ', ''))
    add3 = add.replace('Debrid', 'Real Debrid')
    name2 = quote_plus(name.lower().replace(' ', ''))
    name = name.replace('url', 'URL Resolver')
    menu_items.append((CONFIG.THEME2.format(name.title()), ' '))
    menu_items.append((CONFIG.THEME3.format('Register {0}'.format(add3)), 'RunPlugin(plugin://{0}/?mode=auth{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Save {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=save{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Restore {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=restore{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Import {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=import{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Clear Addon {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=addon{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))

    menu_items.append((CONFIG.THEME2.format('{0} Settings'.format(CONFIG.ADDONTITLE)), 'RunPlugin(plugin://{0}/?mode=settings)'.format(CONFIG.ADDON_ID)))

    return menu_items
