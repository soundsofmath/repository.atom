# -*- coding: utf-8 -*-
"""
    CC_Classic_Cinema
    Copyright (C) 2018,
    Version 1.0.1
    CC
    Jen 2

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    -------------------------------------------------------------

    Returns the CC_Classic_Cinema list-

    <dir>
    <title>CC_Classic_Cinema</title>
    <cc_cinema>all</cc_cinema>
    </dir>

    Genre Lists

    <dir>
    <title>CC_Classic_Cinema Sci-Fi</title>
    <cc_cinema>show|Classic Sci-Fi Movies|appq2OshftHogRH9j</cc_cinema>
    </dir>

    <dir>
    <title>CC_Classic_Cinema Black and White</title>
    <cc_cinema>show|Greatest Black and White Movies of aII time|appj3znDYUUxFmPMC</cc_cinema>
    </dir>

    <dir>
    <title>CC_Classic_Cinema Horror</title>
    <cc_cinema>show|Horror Classic Movies|app0O84HlElrdjgvC</cc_cinema>
    </dir>

    <dir>
    <title>CC_Classic_Cinema Japanese</title>
    <cc_cinema>show|Japanese Monster Movies|appG74t1tzRiXADUK</cc_cinema>
    </dir>

    <dir>
    <title>CC_Classic_Cinema Ray Harryhousen</title>
    <cc_cinema>show|Ray Harryhousen Films|appmFBwFYeMuFZa4z</cc_cinema>
    </dir>
    --------------------------------------------------------------

"""

import requests,re,os,xbmc,xbmcaddon
import base64,pickle,koding,time,sqlite3
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode

CACHE_TIME = 86400  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')

"""
----------------------------------------------------------
"""
table_id = "appkxIBnYZqZpLtLk"
table_name = "CC Classic"
workspace_api_key = "keyC6bZawjvbwgLnw"
"""
----------------------------------------------------------
"""

class CC_Classic_Cinema(Plugin):
    name = "CC_classic_cinema"

    def process_item(self, item_xml):
        if "<cc_cinema>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("cc_cinema", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_cc_cinema_shows",
                    'url': item.get("cc_cinema", ""),
                    'folder': True,
                    'imdb': "0",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item              
            elif "show|" in item.get("cc_cinema", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_cc_cinema_selected_show",
                    'url': item.get("cc_cinema", ""),
                    'folder': True,
                    'imdb': "0",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            
            

@route(mode='open_cc_cinema_shows')
def open_cc_cinema_shows():
    xml = ""
    pins = ""
    at = Airtable(table_id, table_name, api_key=workspace_api_key)
    match = at.get_all(maxRecords=1200, sort=['name'])
    for field in match:
        try:
            res = field['fields']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            summary = res['summary']
            if not summary:
                summary = ""
            else:
                summary = remove_non_ascii(summary)                        
            name = res['name']
            name = remove_non_ascii(name)                                                
            xml += "<item>"\
                   "<title>%s</title>"\
                   "<meta>"\
                   "<content>movie</content>"\
                   "<imdb></imdb>"\
                   "<title></title>"\
                   "<year></year>"\
                   "<thumbnail>%s</thumbnail>"\
                   "<fanart>%s</fanart>"\
                   "<summary>%s</summary>"\
                   "</meta>"\
                   "<cc_cinema>show|%s</cc_cinema>"\
                   "</item>" % (name,thumbnail,fanart,summary,res['link1'])
        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_cc_cinema_selected_show',args=["url"])
def open_selected_show(url):
    xml = ""
    end = url.split("|")[-2].replace(" ","")
    pins = "PLugincccinema"+end
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:
        title = url.split("|")[-2]
        key = url.split("|")[-1]
        result = title
        at = Airtable(key, title, api_key=workspace_api_key)
        match = at.get_all(maxRecords=1200, sort=['name'])
        for field in match:
            try:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                fanart = res['fanart']
                thumbnail = res['thumbnail']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']                                                
                if link2 == "-":
                    xml += "<item>"\
                         "<title>%s</title>"\
                         "<meta>"\
                         "<content>movie</content>"\
                         "<imdb></imdb>"\
                         "<title></title>"\
                         "<year></year>"\
                         "<thumbnail>%s</thumbnail>"\
                         "<fanart>%s</fanart>"\
                         "<summary>%s</summary>"\
                         "</meta>"\
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1)
                elif link3 == "-":
                    xml += "<item>"\
                         "<title>%s</title>"\
                         "<meta>"\
                         "<content>movie</content>"\
                         "<imdb></imdb>"\
                         "<title></title>"\
                         "<year></year>"\
                         "<thumbnail>%s</thumbnail>"\
                         "<fanart>%s</fanart>"\
                         "<summary>%s</summary>"\
                         "</meta>"\
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2) 
                else:
                    xml += "<item>"\
                         "<title>%s</title>"\
                         "<meta>"\
                         "<content>movie</content>"\
                         "<imdb></imdb>"\
                         "<title></title>"\
                         "<year></year>"\
                         "<thumbnail>%s</thumbnail>"\
                         "<fanart>%s</fanart>"\
                         "<summary>%s</summary>"\
                         "</meta>"\
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3)                                      
            except:
                pass                  
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)                       
 
def fetch_from_db2(url):
    koding.reset_db()
    url2 = clean_url(url)
    match = koding.Get_All_From_Table(url2)
    if match:
        match = match[0]
        if not match["value"]:
            return None   
        match_item = match["value"]
        try:
                result = pickle.loads(base64.b64decode(match_item))
        except:
                return None
        created_time = match["created"]
        if float(created_time) + CACHE_TIME <= time.time():
            koding.Remove_Table(url2)
            db = sqlite3.connect('%s' % (database_loc))        
            cursor = db.cursor()
            db.execute("vacuum")
            db.commit()
            db.close()
            return result
        else:
            pass                     
        return result
    else:
        return [] 

def remove_non_ascii(text):
    return unidecode(text)
        
