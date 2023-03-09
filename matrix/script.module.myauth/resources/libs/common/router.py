import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import sys
try:  # Python 3
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    from urlparse import parse_qsl
from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.gui import menu

class Router:
    def __init__(self):
        self.route = None
        self.params = {}

    def _log_params(self, paramstring):
        _url = sys.argv[0]

        self.params = dict(parse_qsl(paramstring))

        logstring = '{0}: '.format(_url)
        for param in self.params:
            logstring += '[ {0}: {1} ] '.format(param, self.params[param])

        logging.log(logstring, level=xbmc.LOGDEBUG)

        return self.params

    def dispatch(self, handle, paramstring):
        self._log_params(paramstring)

        mode = self.params['mode'] if 'mode' in self.params else None
        url = self.params['url'] if 'url' in self.params else None
        name = self.params['name'] if 'name' in self.params else None
        action = self.params['action'] if 'action' in self.params else None

        # MAIN MENU
        if mode is None:
            from resources.libs.gui.main_menu import MainMenu
            MainMenu().get_listing()
            self._finish(handle)


        elif mode == 'trakt':  # Trakt Manager Menu
            menu.trakt_menu()
            self._finish(handle)
            
        elif mode == 'realdebrid':  # Debrid Manager Menu
            menu.debrid_menu()
            self._finish(handle)

            
        # TRAKT MANAGER
        elif mode == 'savetrakt':  # Save Trakt Data
            from resources.libs import traktit
            traktit.trakt_it('update', name)
        elif mode == 'restoretrakt':  # Recover All Saved Trakt Data
            from resources.libs import traktit
            traktit.trakt_it('restore', name)
        elif mode == 'addontrakt':  # Clear All Addon Trakt Data
            from resources.libs import traktit
            traktit.trakt_it('clearaddon', name)
        elif mode == 'cleartrakt':  # Clear All Saved Trakt Data
            from resources.libs import traktit
            traktit.clear_saved(name)
        elif mode == 'updatetrakt':  # Update Saved Trakt Data
            from resources.libs import traktit
            traktit.auto_update('all')

        # DEBRID MANAGER
        elif mode == 'savedebrid':  # Save Debrid Data
            from resources.libs import debridit
            debridit.debrid_it('update', name)
        elif mode == 'restoredebrid':  # Recover All Saved Debrid Data
            from resources.libs import debridit
            debridit.debrid_it('restore', name)
        elif mode == 'restore_myaccts':  # Restore Only Your Accounts Saved Debrid Data
            from resources.libs import debridit_myaccts
            debridit_myaccts.debrid_it('restore', name)
        elif mode == 'addondebrid':  # Clear All Addon Debrid Data
            from resources.libs import debridit
            debridit.debrid_it('clearaddon', name)
        elif mode == 'cleardebrid':  # Clear All Saved Debrid Data
            from resources.libs import debridit
            debridit.clear_saved(name)
        elif mode == 'updatedebrid':  # Update Saved Debrid Data
            from resources.libs import debridit
            debridit.auto_update('all')

        
    def _finish(self, handle):
        from resources.libs.common import directory
        
        directory.set_view()
        
        xbmcplugin.setContent(handle, 'files')
        xbmcplugin.endOfDirectory(handle)                       
