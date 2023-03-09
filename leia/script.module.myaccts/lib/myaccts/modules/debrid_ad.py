import xbmc, xbmcaddon
import xbmcvfs
from pathlib import Path
from myaccts.modules import control


#Seren AD
def serenad_auth():

        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")

                addon = xbmcaddon.Addon("plugin.video.seren")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                enabled_rd = ("false")
                addon.setSetting("realdebrid.enabled", enabled_rd)

                enabled_pm = ("false")
                addon.setSetting("premiumize.enabled", enabled_pm)

                enabled_ad = ("true")
                addon.setSetting("alldebrid.enabled", enabled_ad)

#Ezra AD
def ezraad_auth():

        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ezra/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.ezra")
                addon.setSetting("ad.account_id", your_username)
                addon.setSetting("ad.token", your_token)


#Fen AD
def fenad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.fen")
                addon.setSetting("ad.account_id", your_username)
                addon.setSetting("ad.token", your_token)


#Umbrella AD
def umbad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.umbrella/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.umbrella")
                addon.setSetting("alldebridusername", your_username)
                addon.setSetting("alldebridtoken", your_token)


#Shadow AD
def shadowad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shadow/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.shadow")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)

                
#Ghost AD
def ghostad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.ghost")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Genocide AD
def genocidead_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.Genocide/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.Genocide")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Chains AD
def chainsad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thechains/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.thechains")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Moria AD
def moriaad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.moria/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.moria")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Base 19 AD
def basead_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.base19/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.base19")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Twisted AD
def twistedad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.twisted/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.twisted")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Magic Dragon AD
def mdad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.magicdragon/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Asgard AD
def asgardad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.asgard/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.asgard")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#M.E.T.V AD
def metvad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.metv19/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.metv19")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#ResolveURL AD
def rurlad_auth():
        
        file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')

        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.ghost")
                addon.setSetting("AllDebridResolver_client_id", your_username)
                addon.setSetting("AllDebridResolver_token", your_token)

                cache_only = ("true")
                addon.setSetting("AllDebridResolver_cached_only", cache_only)


#My Accounts AD
def myaccountsad_auth():

        file = xbmcvfs.translatePath('special://userdata/addon_data/script.module.myaccounts/settings.xml')
        
        if xbmcvfs.exists(file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("script.module.myaccounts")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)


def save_data_backup():

        xbmc.executebuiltin('PlayMedia(plugin://script.module.myauth/?mode=savedebrid&name=all)') #Backup debrid data to wizard directory


def restore_myaccts_backup():

        xbmc.executebuiltin('PlayMedia(plugin://script.module.myauth/?mode=restore_myaccts&name=all)') #Restore Your Accounts Data Only
        xbmc.sleep(2000)


def debrid_auth_ad():

        #AllDebrid
        serenad_auth()
        ezraad_auth()
        fenad_auth()
        umbad_auth()
        shadowad_auth()
        ghostad_auth()
        genocidead_auth()
        chainsad_auth()
        moriaad_auth()
        basead_auth()
        twistedad_auth()
        mdad_auth()
        asgardad_auth()
        metvad_auth()
        rurlad_auth()
        myaccountsad_auth()
        save_data_backup()

def debrid_restore_ad():

        #AllDebrid
        restore_myaccts_backup()
        serenad_auth()
        ezraad_auth()
        fenad_auth()
        umbad_auth()
        shadowad_auth()
        ghostad_auth()
        genocidead_auth()
        chainsad_auth()
        moriaad_auth()
        basead_auth()
        twistedad_auth()
        mdad_auth()
        asgardad_auth()
        metvad_auth()
        rurlad_auth()
        myaccountsad_auth()
        save_data_backup()

exit

