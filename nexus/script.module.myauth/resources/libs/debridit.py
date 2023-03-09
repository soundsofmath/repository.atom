import xbmc
import xbmcaddon
import xbmcgui

import os
import time

from xml.etree import ElementTree

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools

ORDER = ['serenrd', 'serenpm', 'serenad',
         'ezrard', 'ezrapm', 'ezraad',
         'fenrd', 'fenpm', 'fenad',
         'umbrd', 'umbpm', 'umbad',
         'shadowrd', 'shadowpm', 'shadowad',
         'ghostrd', 'ghostpm', 'ghostad',
         'genociderd', 'genocidepm', 'genocidead',
         'chainsrd', 'chainspm', 'chainsad',
         'base19rd', 'base19pm', 'base19ad',
         'twistedrd', 'twistedpm', 'twistedad',
         'mdrd', 'mdpm', 'mdad',
         'asgardrd', 'asgardpm', 'asgardad',
         'metvrd', 'metvpm', 'metvad',
         'myactrd', 'myactpm', 'myactad',
         'mactrd', 'mactpm', 'mactad',
         'rurlrd', 'rurlpm', 'rurlad',
         'premiumizer',]

DEBRIDID = {
    'serenrd': {
        'name'     : 'Seren RD',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'ico-seren-2.jpg'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'fanart-seren-2.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'seren_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'rd.username',
        'data'     : ['rd.auth', 'rd.client_id', 'rd.expiry', 'rd.refresh', 'rd.secret', 'rd.username', 'realdebrid.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.seren)'},
    'serenpm': {
        'name'     : 'Seren PM',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'ico-seren-2.jpg'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'fanart-seren-2.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'seren_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.enabled', 'premiumize.username', 'premiumize.token'],
        'activate' : 'Addon.OpenSettings(plugin.video.seren)'},
    'serenad': {
        'name'     : 'Seren AD',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'ico-seren-2.jpg'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'fanart-seren-2.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'seren_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.enabled', 'alldebrid.username', 'alldebrid.token'],
        'activate' : 'Addon.OpenSettings(plugin.video.seren)'},
    'ezrard': {
        'name'     : 'Ezra RD',
        'plugin'   : 'plugin.video.ezra',
        'saved'    : 'ezrard',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'ezra_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ezra', 'settings.xml'),
        'default'  : 'rd.username',
        'data'     : ['rd.username', 'rd.token', 'rd.client_id', 'rd.refresh', 'rd.secret','rd.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.ezra)'},
    'ezrapm': {
        'name'     : 'Ezra PM',
        'plugin'   : 'plugin.video.ezra',
        'saved'    : 'ezrapm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'ezra_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ezra', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.account_id', 'pm.token', 'pm.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.ezra)'},
    'ezraad': {
        'name'     : 'Ezra AD',
        'plugin'   : 'plugin.video.ezra',
        'saved'    : 'ezraad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'ezra_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ezra', 'settings.xml'),
        'default'  : 'ad.account_id',
        'data'     : ['ad.account_id', 'ad.token'],
        'activate' : 'Addon.OpenSettings(plugin.video.ezra)'},
    'fenrd': {
        'name'     : 'Fen RD',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'fen_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'rd.account_id',
        'data'     : ['rd.client_id', 'rd.refresh', 'rd.secret', 'rd.token', 'rd.account_id', 'rd.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'fenpm': {
        'name'     : 'Fen PM',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'fen_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.token', 'pm.account_id', 'pm.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'fenad': {
        'name'     : 'Fen AD]',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'fen_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'ad.account_id',
        'data'     : ['ad.token', 'ad.enabled', 'ad.account_id'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'umbrd': {
        'name'     : 'Umbrella RD',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umbrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'umb_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'realdebridusername',
        'data'     : ['realdebridusername', 'realdebridtoken', 'realdebrid.clientid', 'realdebridsecret', 'realdebridrefresh', 'realdebrid.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'umbpm': {
        'name'     : 'Umbrella PM',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umbpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'umb_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'premiumizeusername',
        'data'     : ['premiumizeusername', 'premiumizetoken', 'premiumize.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'umbad': {
        'name'     : 'Umbrella AD',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umbad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'umb_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'alldebridusername',
        'data'     : ['alldebridusername', 'alldebridtoken'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'shadowrd': {
        'name'     : 'Shadow RD',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'shadow_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.shadow)'},
    'shadowpm': {
        'name'     : 'Shadow PM',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'shadow_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.shadow)'},
    'shadowad': {
        'name'     : 'Shadow AD',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'shadow_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.shadow)'},
    'ghostrd': {
        'name'     : 'Ghost RD',
        'plugin'   : 'plugin.video.ghost',
        'saved'    : 'ghostrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'ghost_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shost', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.ghost)'},
    'ghostpm': {
        'name'     : 'Ghost PM',
        'plugin'   : 'plugin.video.ghost',
        'saved'    : 'ghostpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'ghost_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ghost', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.ghost)'},
    'ghostad': {
        'name'     : 'Ghost AD',
        'plugin'   : 'plugin.video.ghost',
        'saved'    : 'ghostad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'ghost_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ghost', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.ghost)'},
    'genociderd': {
        'name'     : 'Genocide RD',
        'plugin'   : 'plugin.video.Genocide',
        'saved'    : 'genociderd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'genocide_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.Genocide', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.Genocide)'},
    'genocidepm': {
        'name'     : 'Genocide PM',
        'plugin'   : 'plugin.video.Genocide',
        'saved'    : 'genocidepm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'genocide_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.Genocide', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.Genocide)'},
    'genocidead': {
        'name'     : 'Genocide AD',
        'plugin'   : 'plugin.video.Genocide',
        'saved'    : 'genocidead',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'genocide_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.Genocide', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.Genocide)'},
    'chainsrd': {
        'name'     : 'Chains Lite RD',
        'plugin'   : 'plugin.video.thechains',
        'saved'    : 'chainsrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'chains_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thechains', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.thechains)'},
    'chainspm': {
        'name'     : 'Chains Lite PM',
        'plugin'   : 'plugin.video.thechains',
        'saved'    : 'chainspm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'chains_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thechains', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.thechains)'},
    'chainsad': {
        'name'     : 'Chains Lite AD',
        'plugin'   : 'plugin.video.thechains',
        'saved'    : 'chainsad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'chains_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thechains', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.thechains)'},
    'base19rd': {
        'name'     : 'Base 19 RD',
        'plugin'   : 'plugin.video.base19',
        'saved'    : 'base19rd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'base19_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.base19', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.base19)'},
    'base19pm': {
        'name'     : 'Base 19 PM',
        'plugin'   : 'plugin.video.base19',
        'saved'    : 'base19pm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'base19_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.base19', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.base19)'},
    'base19ad': {
        'name'     : 'Base 19 AD',
        'plugin'   : 'plugin.video.base19',
        'saved'    : 'base19',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'base19_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.base19', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.base19)'},
    'twistedrd': {
        'name'     : 'Twisted RD',
        'plugin'   : 'plugin.video.twisted',
        'saved'    : 'twistedrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'twisted_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.twisted', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.twisted)'},
    'twistedpm': {
        'name'     : 'Twisted PM',
        'plugin'   : 'plugin.video.twisted',
        'saved'    : 'twistedpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'twisted_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.twisted', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.twisted)'},
    'twistedad': {
        'name'     : 'Twisted AD',
        'plugin'   : 'plugin.video.twisted',
        'saved'    : 'twistedad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'twisted_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.twisted', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.twisted)'},
    'mdrd': {
        'name'     : 'Magic Dragon RD',
        'plugin'   : 'plugin.video.magicdragon',
        'saved'    : 'mdrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'md_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.magicdragon', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.magicdragon)'},
    'mdpm': {
        'name'     : 'Magic Dragon PM',
        'plugin'   : 'plugin.video.magicdragon',
        'saved'    : 'mdpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'md_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.magicdragon', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.magicdragon)'},
    'mdad': {
        'name'     : 'Magic Dragon AD',
        'plugin'   : 'plugin.video.magicdragon',
        'saved'    : 'mdad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'md_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.magicdragon', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.magicdragon)'},
    'asgardrd': {
        'name'     : 'Asgard RD',
        'plugin'   : 'plugin.video.asgard',
        'saved'    : 'asgardrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'asgard_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.asgard', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.asgard)'},
    'asgardpm': {
        'name'     : 'Asgard PM',
        'plugin'   : 'plugin.video.asgard',
        'saved'    : 'asgardpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'asgard_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.asgard', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.asgard)'},
    'asgardad': {
        'name'     : 'Asgard AD',
        'plugin'   : 'plugin.video.asgard',
        'saved'    : 'asgardad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'asgard_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.asgard', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.asgard)'},
    'metvrd': {
        'name'     : 'M.E.T.V RD',
        'plugin'   : 'plugin.video.metv19',
        'saved'    : 'metvrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'metv_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.metv19', 'settings.xml'),
        'default'  : 'rd.client_id',
        'data'     : ['rd.expiry', 'rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.metv19)'},
    'metvpm': {
        'name'     : 'M.E.T.V PM',
        'plugin'   : 'plugin.video.metv19',
        'saved'    : 'metvpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'metv_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.metv19', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.metv19)'},
    'metvad': {
        'name'     : 'M.E.T.V AD',
        'plugin'   : 'plugin.video.metv19',
        'saved'    : 'metvad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'metv_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.metv19', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.metv19)'},
    'myactrd': {
        'name'     : 'My Accounts RD',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myactrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'myact_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : 'realdebrid.username',
        'data'     : ['realdebrid.client_id', 'realdebrid.refresh', 'realdebrid.secret', 'realdebrid.token', 'realdebrid.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'},
   'myactpm': {
        'name'     : 'My Accounts PM',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myactpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'myact_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.token', 'premiumize.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'},
   'myactad': {
        'name'     : 'My Accounts AD',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myactad',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'myact_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.token', 'alldebrid.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'},
    'mactrd': {
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
   'mactpm': {
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
   'mactad': {
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
        'activate' : 'Addon.OpenSettings(script.module.myaccts)'},
    'rurlrd': {
        'name'     : 'ResolveURL RD',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'rurl_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'RealDebridResolver_client_id',
        'data'     : ['RealDebridResolver_client_id', 'RealDebridResolver_client_secret', 'RealDebridResolver_enabled', 'RealDebridResolver_refresh', 'RealDebridResolver_token', 'RealDebridResolver_cached_only'],
        'activate' : 'Addon.OpenSettings(script.module.resolveurl)'},
    'rurlpm': {
        'name'     : 'ResolveURL PM',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'rurl_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'PremiumizeMeResolver_token',
        'data'     : ['PremiumizeMeResolver_token', 'PremiumizeMeResolver_cached_only'],
        'activate' : 'Addon.OpenSettings(script.module.resolveurl)'},
    'rurlad': {
        'name'     : 'ResolveURL AD',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlad',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'rurl_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'AllDebridResolver_client_id',
        'data'     : ['AllDebridResolver_client_id', 'AllDebridResolver_enabled', 'AllDebridResolver_login', 'AllDebridResolver_priority', 'AllDebridResolver_token', 'AllDebridResolver_torrents', 'AllDebridResolver_cached_only'],
        'activate' : 'Addon.OpenSettings(script.module.resolveurl)'},
   'premiumizer': {
	'name'     : 'Premiumizer',
	'plugin'   : 'plugin.video.premiumizerx',
	'saved'    : 'premiumizer',
	'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx'),
	'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx', 'icon.png'),
	'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx', 'fanart.jpg'),
	'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'premiumizer_pm'),
	'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizerx', 'settings.xml'),
	'default'  : 'premiumize.token',
	'data'     : ['premiumize.status', 'premiumize.token', 'premiumize.refresh'],
	'activate' : 'Addon.OpenSettings(plugin.video.premiumizerx)'}
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
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, DEBRIDID[who]['name']),
                               '[COLOR {0}]Debrid Info: Removed![/COLOR]'.format(CONFIG.COLOR2),
                               2000,
                               DEBRIDID[who]['icon'])
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
