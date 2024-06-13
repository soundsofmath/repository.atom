import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import os.path

joinPath = os.path.join
dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon
addonObject = addon('script.module.myaccts')
addonInfo = addonObject.getAddonInfo
rd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'realdebrid.png')
pm_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'premiumize.png')
ad_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'alldebrid.png')

def notification(title=None, message=None, icon=None, time=3000, sound=False):
	if title == 'default' or title is None: title = addonName()
	if isinstance(title, int): heading = lang(title)
	else: heading = str(title)
	if isinstance(message, int): body = lang(message)
	else: body = str(message)
	if icon is None or icon == '' or icon == 'default': icon = addonIcon()
	elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
	elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
	elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
	dialog.notification(heading, body, icon, time, sound=sound)

def addonIcon():
	return addonInfo('icon')

def addonName():
	return addonInfo('name')

def realdebrid():
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.program.709wizard/debrid/myact_rd')

        if xbmcvfs.exists(file):
                accounts = xbmcaddon.Addon('script.module.myaccts').getSetting("realdebrid.token")
                if not accounts:
                        xbmc.sleep(25000)
                        from myaccts.modules import debrid_rd
                        debrid_rd.debrid_restore_rd()
                        notification('RealDebrid', 'Debrid Data Restored!', icon=pm_icon)

def premiumize():
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.program.709wizard/debrid/myact_pm')

        if xbmcvfs.exists(file):
                accounts = xbmcaddon.Addon('script.module.myaccts').getSetting("premiumize.token")
                if not accounts:
                        xbmc.sleep(25000)
                        from myaccts.modules import debrid_pm
                        debrid_pm.debrid_restore_pm()
                        notification('Premiumize', 'Debrid Data Restored!', icon=pm_icon)


def alldebrid():
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.program.709wizard/debrid/myact_ad')

        if xbmcvfs.exists(file):
                accounts = xbmcaddon.Addon('script.module.myaccts').getSetting("alldebrid.token")
                if not accounts:
                        xbmc.sleep(25000)
                        from myaccts.modules import debrid_ad
                        debrid_ad.debrid_restore_ad()
                        notification('AllDebrid', 'Debrid Data Restored!', icon=pm_icon)


realdebrid()
premiumize()
alldebrid()

exit




