import xbmc
import xbmcaddon
import xbmcgui
import os
import time
from xml.etree import ElementTree
from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools

ORDER = ['myactrd', 'myactpm', 'myactad',]

DEBRIDID = {
    'myactrd': {
        'name'     : 'Your Accounts RD',
        'plugin'   : 'script.module.myaccts',
        'saved'    : 'myactrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'myact_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccts', 'settings.xml'),
        'default'  : 'realdebrid.username',
        'data'     : ['realdebrid.client_id', 'realdebrid.refresh', 'realdebrid.secret', 'realdebrid.token', 'realdebrid.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccts)'},
   'myactpm': {
        'name'     : 'Your Accounts PM',
        'plugin'   : 'script.module.myaccts',
        'saved'    : 'myactpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'myact_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccts', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.token', 'premiumize.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccts)'},
   'myactad': {
        'name'     : 'Your Accounts AD',
        'plugin'   : 'script.module.myaccts',
        'saved'    : 'myactad',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'myact_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccts', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.token', 'alldebrid.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccts)'}
}


def debrid_user(who):
    user = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user = add.getSetting(DEBRIDID[who]['default'])
            except:
                pass
    return user


def debrid_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.DEBRIDFOLD):
        os.makedirs(CONFIG.DEBRIDFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(DEBRIDID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(DEBRIDID[log]['plugin'])
                    default = DEBRIDID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_debrid(do, log)
                except:
                    pass
            else:
                logging.log('[Debrid Info] {0}({1}) is not installed'.format(DEBRIDID[log]['name'], DEBRIDID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('debridnextsave', tools.get_date(days=3, formatted=True))
    else:
        if DEBRIDID[who]:
            if os.path.exists(DEBRIDID[who]['path']):
                update_debrid(do, who)
        else:
            logging.log('[Debrid Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)


def clear_saved(who, over=False):
    if who == 'all':
        for debrid in DEBRIDID:
            clear_saved(debrid,  True)
    elif DEBRIDID[who]:
        file = DEBRIDID[who]['file']
        if os.path.exists(file):
            os.remove(file)
        CONFIG.set_setting(DEBRIDID[who]['saved'], '')
    if not over:
        xbmc.executebuiltin('Container.Refresh()')


def update_debrid(do, who):
    file = DEBRIDID[who]['file']
    settings = DEBRIDID[who]['settings']
    data = DEBRIDID[who]['data']
    addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
    saved = DEBRIDID[who]['saved']
    default = DEBRIDID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = DEBRIDID[who]['name']
    icon = DEBRIDID[who]['icon']

    if do == 'update':
        if not user == '':
            try:
                root = ElementTree.Element(saved)
                
                for setting in data:
                    debrid = ElementTree.SubElement(root, 'debrid')
                    id = ElementTree.SubElement(debrid, 'id')
                    id.text = setting
                    value = ElementTree.SubElement(debrid, 'value')
                    value.text = addonid.getSetting(setting)
                  
                tree = ElementTree.ElementTree(root)
                tree.write(file)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                
                logging.log('Debrid Info Saved for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Debrid Info Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('debrid'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('Debrid Info Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Debrid Info Not Found for {0}'.format(name))
    elif do == 'clearaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings))
        if os.path.exists(settings):
            try:
                tree = ElementTree.parse(settings)
                root = tree.getroot()
                
                for setting in root.findall('setting'):
                    if setting.attrib['id'] in data:
                        logging.log('Removing Setting: {0}'.format(setting.attrib))
                        root.remove(setting)
                            
                tree.write(settings)
                
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Addon Data: Cleared![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
    xbmc.executebuiltin('Container.Refresh()')


def auto_update(who):
    if who == 'all':
        for log in DEBRIDID:
            if os.path.exists(DEBRIDID[log]['path']):
                auto_update(log)
    elif DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            u = debrid_user(who)
            su = CONFIG.get_setting(DEBRIDID[who]['saved'])
            n = DEBRIDID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                debrid_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]Debrid Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springreen]Save Debrid[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No, Cancel[/COLOR][/B]"):
                    debrid_it('update', who)
            else:
                debrid_it('update', who)


def import_list(who):
    if who == 'all':
        for log in DEBRIDID:
            if os.path.exists(DEBRIDID[log]['file']):
                import_list(log)
    elif DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['file']):
            file = DEBRIDID[who]['file']
            addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
            saved = DEBRIDID[who]['saved']
            default = DEBRIDID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = DEBRIDID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('debrid'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]Debrid Info: Imported![/COLOR]'.format(CONFIG.COLOR2))


def activate_debrid(who):
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            act = DEBRIDID[who]['activate']
            addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
            if act == '':
                addonid.openSettings()
            else:
                xbmc.executebuiltin(DEBRIDID[who]['activate'])
        else:
            dialog = xbmcgui.Dialog()

            dialog.ok(CONFIG.ADDONTITLE,
                          '{0} is not currently installed.'.format(DEBRIDID[who]['name']))
    else:
        xbmc.executebuiltin('Container.Refresh()')
        return

    check = 0
    while not debrid_user(who):
        if check == 30:
            break
        check += 1
        time.sleep(10)
    xbmc.executebuiltin('Container.Refresh()')
