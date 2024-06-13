import xbmc, xbmcaddon
import xbmcvfs
from pathlib import Path
from myaccts.modules import control


#Seren PM
def serenpm_auth():

        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')
        
        if xbmcvfs.exists(file):
                
                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")

                addon = xbmcaddon.Addon("plugin.video.seren")
                addon.setSetting("premiumize.username", your_username)
                addon.setSetting("premiumize.token", your_token)

                enabled_rd = ("false")
                addon.setSetting("realdebrid.enabled", enabled_rd)

                enabled_pm = ("true")
                addon.setSetting("premiumize.enabled", enabled_pm)

                enabled_ad = ("false")
                addon.setSetting("alldebrid.enabled", enabled_ad)


#Ezra PM
def ezrapm_auth():

        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ezra/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.ezra")
                addon.setSetting("pm.account_id", your_username)
                addon.setSetting("pm.token", your_token)


#Fen PM
def fenpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.fen")
                addon.setSetting("pm.account_id", your_username)
                addon.setSetting("pm.token", your_token)


#Umbrella PM
def umbpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.umbrella/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.umbrella")
                addon.setSetting("premiumizeusername", your_username)
                addon.setSetting("premiumizetoken", your_token)


#Shadow PM
def shadowpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shadow/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.shadow")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)

                
#Ghost PM
def ghostpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.ghost")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Genocide PM
def genocidepm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.Genocide/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.Genocide")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Chains PM
def chainspm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thechains/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.thechains")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Moria PM
def moriapm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.moria/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.moria")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Base19 PM
def basepm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.base19/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.base19")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Twisted PM
def twistedpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.twisted/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.twisted")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Magic Dragon PM
def mdpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.magicdragon/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Asgard PM
def asgardpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.asgard/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.asgard")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#M.E.T.V PM
def metvpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.metv19/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.metv19")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#ResolveURL PM
def rurlpm_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/script.module.resolveurl/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("script.module.resolveurl")
                addon.setSetting("premiumize.username", your_username)
                addon.setSetting("PremiumizeMeResolver_token", your_token)

                cache_only = ("true")
                addon.setSetting("PremiumizeMeResolver_cached_only", cache_only)


#My Accounts PM
def myaccountspm_auth():

        file = xbmcvfs.translatePath('special://userdata/addon_data/script.module.myaccounts/settings.xml')
        
        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("script.module.myaccounts")
                addon.setSetting("premiumize.username", your_username)

                your_token = myaccts.getSetting("premiumize.token")
                addon.setSetting("premiumize.token", your_token)


#Premiumizer PM
def premiumizer_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.premiumizer/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.premiumizer")
                addon.setSetting("premiumize.token", your_token)


def save_data_backup():

        xbmc.executebuiltin('PlayMedia(plugin://script.module.myauth/?mode=savedebrid&name=all)') #Backup debrid data to wizard directory


def restore_myaccts_backup():

        xbmc.executebuiltin('PlayMedia(plugin://script.module.myauth/?mode=restore_myaccts&name=all)') #Restore Your Accounts Data Only
        xbmc.sleep(2000)


def debrid_auth_pm():

        #Premiumize       
        serenpm_auth()
        ezrapm_auth()
        fenpm_auth()
        umbpm_auth()
        shadowpm_auth()
        ghostpm_auth()
        genocidepm_auth()
        chainspm_auth()
        moriapm_auth()
        basepm_auth()
        twistedpm_auth()
        mdpm_auth()
        asgardpm_auth()
        metvpm_auth()
        rurlpm_auth()
        myaccountspm_auth()
        premiumizer_auth()
        save_data_backup()

def debrid_restore_pm():

        #Premiumize
        restore_myaccts_backup()
        serenpm_auth()
        ezrapm_auth()
        fenpm_auth()
        umbpm_auth()
        ghostpm_auth()
        shadowpm_auth()
        genocidepm_auth()
        chainspm_auth()
        moriapm_auth()
        basepm_auth()
        twistedpm_auth()
        mdpm_auth()
        asgardpm_auth()
        metvpm_auth()
        rurlpm_auth()
        myaccountspm_auth()
        premiumizer_auth()
        save_data_backup()

exit

