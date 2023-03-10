# -*- coding: utf-8 -*-
"""
    tmdb.py --- Jen Plugin for accessing tmdb data
    Copyright (C) 2017, Jen

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
    
    Version:
        2019-07-18
            - Updated so that season and episode numbers less than 10 are displayed as double digits with a leading "0" (example: Season 1, Episode 9 ==> S01E09) (same as trakt.py)
            - Categorized Usage Examples
        2018-07-02
            - Updated Clear Cache Hook
        2018-06-26
            - Added customizable settings for 2 colors (COLOR1 for Movie/Show titles; COLOR2 for Season/Episode numbers as well as for "Next Page >>")
            - Added Year in () to end of titles for both TV Shows & Movies (including Trailers) 
            - Updated the display for seasons (added ":" between season and season number) as well as for episodes (added season & episode number to title)
            - Added thumbnail for "Next Page >>" (same as imdb.py)
        2018-05-14
            Latest version to include with a Jen Release

    -------------------------------------------------------------

    *** COLORS ***
        Set your desired colors for the COLOR1 & COLOR2 variables within "" on lines 210 & 211 below.
        COLOR1 is for Movie/Show titles; COLOR2 is for Season/Episode numbers as well as for "Next Page >>".
        The color values can be alphanumeric (example: red, limegreen) or Hex (example: ffff0000, FF00FF00).
        If colors are left blank, they will display as the default color set within the skin you're using.
        
        -- Note:  In order for the Color settings to work as intended, Metadata must be DISABLED in the addon settings!!!

    -------------------------------------------------------------

    Usage Examples:


	### Search ###
	
	** Returns a list of items Searched for from TMDB
	<dir>
	  <title>Search TMDB</title>
	  <tmdb>search</tmdb>
	</dir>


	### Movies ###
	
	** Returns a list of Now Playing Movies
	<dir>
	  <title>TMDB Movies Now Playing</title>
	  <tmdb>movies/now_playing</tmdb>
	</dir>

	** Returns a list of the TMDB Most Popular Movies
	<dir>
	  <title>TMDB Popular Movies</title>
	  <tmdb>movies/popular</tmdb>
	</dir>

	** Returns a list of the TMDB Top Rated Movies
	<dir>
	  <title>TMDB Top Rated Movies</title>
	  <tmdb>movies/top_rated</tmdb>
	</dir>

	** Returns upcoming movies, then Trailers for the movies.  Second Tag must be movie/upcoming
	<dir>
	  <title>TMDB Upcoming Movies</title>
	  <tmdb>movie/upcoming</tmdb>
	  <summary>Shows Trailers For Upcoming Movies</summary>
	</dir>

	** Returns a list of the TMDB Popular People Movies.  Results show only Movie Titles currently.
	<dir>
	  <title>TMDB Popular People Movies</title>
	  <tmdb>people/popular</tmdb>
	</dir>

	** Returns a list of the TMDB Movies by a specific Year.  Must change Year at the end Of the Second Tag.
	<dir>
	  <title>Movies Released In 2018</title>
	  <tmdb>year/movies/2018</tmdb>
	</dir>

	** Returns a list of Movies by a specific Genre.  Must change Genre ID at the end Of the Second Tag.
	<dir>
	  <title>TMDB Action Movies</title>
	  <tmdb>genre/movies/28</tmdb>
	</dir>

	** Returns a list of Movies by a Specific Actor.  Must change Actor ID at the end Of the Second Tag.
	<dir>
	  <title>Al Pacino</title>
	  <tmdb>person/movies/1158</tmdb>
	</dir>

	** Returns a list of Movies by a Production Companies.  Must change Production Company ID at the end Of the Second Tag.
	<dir>
		<title>Pixar Animation</title>
		<tmdb>company/movies/3</tmdb>
	</dir>

	** Returns a list of a specific Movie Collection.  Must change Movie Collection ID at the end Of the Second Tag.
	<dir>
	  <title>TMDB Star Wars Collection</title>
	  <tmdb>collection/10</tmdb>
	</dir>

	** Returns a list of Movies by a specific Keyword.  Must change Keyword ID at the end of the Second Tag.
	<dir>
	  <title>TMDB Army Movies</title>
	  <tmdb>keyword/movies/6092</tmdb>
	</dir>

	** Returns the Trailer for a specific Movie.   Must change Movie Trailer ID at the end of the Second Tag.
	<dir>
	  <title>Star Wars: The Last Jedi TRAILER</title>
	  <tmdb>trailer/181808</tmdb>
	</dir>


	### TV Shows ###
	
	** Returns a list of TV Shows Airing Today
	<dir>
	  <title>TMDB Shows Airing Today</title>
	  <tmdb>tv/today</tmdb>
	</dir>

	** Returns a list of the TMDB Popular TV Shows
	<dir>
	  <title>TMDB Popular Shows</title>
	  <tmdb>tv/popular</tmdb>
	</dir>

	** Returns a list of the TMDB Top Rated TV Shows
	<dir>
	  <title>TMDB Top Rated Shows</title>
	  <tmdb>tv/top_rated</tmdb>
	</dir>

	** Returns a list of the TMDB TV Shows Airing in the Next 7 Days
	<dir>
	  <title>TMDB Shows On The Air</title>
	  <tmdb>tv/on_the_air</tmdb>
	</dir>

	** Returns a list of the TMDB TV Shows by Genre.  Must change Genre ID at the end of the second Tag
	<dir>
	  <title>TMDB Animation Shows</title>
	  <tmdb>genre/shows/16</tmdb>
	</dir>

	** Returns a list of the TMDB TV Shows by Network.  Must change Network ID at the end of the second Tag
	<dir>
		<title>ABC</title>
		<tmdb>network/shows/2</tmdb>
	</dir>

	** Returns a list of the TMDB TV Shows by Actor.  Must change Actor ID at the end of the second Tag
	<dir>
	  <title>TMDB Bryan Cranston Shows</title>
	  <tmdb>person/shows/17419</tmdb>
	</dir>

	** Returns a list of the TMDB TV Shows by a specific Keyword.  Must change Keyword ID At The End Of The Second Tag
	<dir>
	  <title>TMDB King Shows</title>
	  <tmdb>keyword/shows/13084</tmdb>
	</dir>

	** Returns a list of the TMDB Animal Kingdom TV Shows.  Must change List ID at the end of the second Tag
	<dir>
	  <title>TMDB List: Animal Kingdom</title>
	  <tmdb>list/13488</tmdb>
	</dir>

    -------------------------------------------------------------
"""

import __builtin__
import pickle
import base64
import time

import koding
import resources.lib.external.tmdbsimple as tmdbsimple
import xbmcaddon, xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
COLOR1 = "lightgrey"
COLOR2 = "turquoise"


class TMDB(Plugin):
    name = "tmdb"

    def process_item(self, item_xml):
        if "<tmdb>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "tmdb",
                'url': item.get("tmdb", ""),
                'folder': True,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "tmdb_tv_show" in item_xml:
            item = JenItem(item_xml)
            url = item.get("link", ")").replace("tmdb_tv_show(", "")[:-1]
            result_item = {
                'label': item["title"],
                'icon': item["thumbnail"],
                'fanart': item.get("fanart", addon_fanart),
                'mode': "tmdb_tv_show",
                'url': "tmdb_id" + url,
                'folder': True,
                'content': "tvshows",
                'season': "0",
                'episode': "0",
                'info': {},
                "imdb": item.get("imdb", "0"),
                'year': item.get("year", ""),
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "tmdb_season(" in item_xml:
            item = JenItem(item_xml)
            url = item.get("link", ")").replace("tmdb_season(", "")[:-1]
            season = url.split(",")[1]
            result_item = {
                'label': item["title"],
                'icon': item["thumbnail"],
                'fanart': item.get("fanart", addon_fanart),
                'mode': "tmdb_season",
                'url': "tmdb_id" + url,
                'folder': True,
                'content': "seasons",
                'season': str(season),
                'episode': "0",
                'info': {},
                "imdb": item.get("imdb", "0"),
                'year': item.get("year", ""),
                'context': {},
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item

    def clear_cache(self):
        skip_prompt = xbmcaddon.Addon().getSetting("quiet_cache")
        dialog = xbmcgui.Dialog()
        if skip_prompt == 'false':
            if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear TMDB Plugin Cache?"):
                koding.Remove_Table("tmdb_plugin")
        else:
            koding.Remove_Table("tmdb_plugin")


@route(mode='tmdb', args=["url"])
def tmdb(url):
    pins = ""
    page = 1
    try:
        xml, __builtin__.content_type = fetch_from_db(url) or (None, None)
    except Exception:
        xml, __builtin__.content_type = None, None
    if not xml:
        content = "files"
        xml = ""
        response = None
        if url.startswith("movies"):
            if url.startswith("movies/popular"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.Movies().popular(page=page)
            if url.startswith("movies/now_playing"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.Movies().now_playing(page=page)
            if url.startswith("movies/top_rated"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.Movies().top_rated(page=page)

            for item in response["results"]:
                xml += get_movie_xml(item)
                content = "movies"
        elif url.startswith("people"):
            if url.startswith("people/popular"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.People().popular(page=page)
            for item in response["results"]:
                xml += get_person_xml(item)
                content = "movies"
        elif url.startswith("movie"):
            if url.startswith("movie/upcoming"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.Movies().upcoming(page=page)
            for item in response["results"]:
                xml += get_trailer_xml(item)
                content = "movies"
        elif url.startswith("tv"):
            if url.startswith("tv/popular"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.TV().popular(page=page)
            elif url.startswith("tv/top_rated"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.TV().top_rated(page=page)
            elif url.startswith("tv/today"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.TV().airing_today(page=page)
            elif url.startswith("tv/on_the_air"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.TV().on_the_air(page=page)
            for item in response["results"]:
                xml += get_show_xml(item)
                content = "tvshows"
        elif url.startswith("list"):
            list_id = url.split("/")[-1]
            if not response:
                response = tmdbsimple.Lists(list_id).info()
            for item in response.get("items", []):
                if "title" in item:
                    xml += get_movie_xml(item)
                    content = "movies"
                elif "name" in item:
                    xml += get_show_xml(item)
                    content = "tvshows"
        elif url.startswith("trailer"):
            movie_id = url.split("/")[-1]
            if not response:
                response = tmdbsimple.Movies(movie_id).videos()
            for item in response["results"]:
                if "type" in item:
                    xml += get_trailer_video_xml(item)
                    content = "movies"
        elif url.startswith("person"):
            split_url = url.split("/")
            person_id = split_url[-1]
            media = split_url[-2]
            if media == "movies":
                if not response:
                    response = tmdbsimple.People(person_id).movie_credits()
            elif media == "shows":
                if not response:
                    response = tmdbsimple.People(person_id).tv_credits()

            for job in response:
                if job == "id":
                    continue
                for item in response[job]:
                    if media == "movies":
                        xml += get_movie_xml(item)
                        content = "movies"
                    elif media == "shows":
                        xml += get_show_xml(item)
                        content = "tvshows"
        elif url.startswith("genre"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            genre_id = split_url[-2]
            media = split_url[-3]
            if media == "movies":
                if not response:
                    response = tmdbsimple.Discover().movie(with_genres=genre_id, page=page)
            elif media == "shows":
                if not response:
                    response = tmdbsimple.Discover().tv(with_genres=genre_id, page=page)
            for item in response["results"]:
                if media == "movies":
                    xml += get_movie_xml(item)
                    content = "movies"
                elif media == "shows":
                    xml += get_show_xml(item)
                    content = "tvshows"
        elif url.startswith("year"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            release_year = split_url[-2]
            media = split_url[-3]
            if media == "movies":
                if not response:
                    response = tmdbsimple.Discover().movie(primary_release_year=release_year, page=page)
            for item in response["results"]:
                if media == "movies":
                    xml += get_movie_xml(item)
                    content = "movies"
        elif url.startswith("network"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            network_id = split_url[-2]
            media = split_url[-3]
            if media == "shows":
                if not response:
                    response = tmdbsimple.Discover().tv(with_networks=network_id, page=page)
            for item in response["results"]:
                if media == "shows":
                    xml += get_show_xml(item)
                    content = "tvshows"
        elif url.startswith("company"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            company_id = split_url[-2]
            media = split_url[-3]
            if media == "movies":
                if not response:
                    response = tmdbsimple.Discover().movie(with_companies=company_id, page=page)
            for item in response["results"]:
                if media == "movies":
                    xml += get_movie_xml(item)
                    content = "movies"
        elif url.startswith("keyword"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            keyword_id = split_url[-2]
            media = split_url[-3]
            if media == "movies":
                if not response:
                    response = tmdbsimple.Discover().movie(with_keywords=keyword_id, page=page)
            elif media == "shows":
                if not response:
                    response = tmdbsimple.Discover().tv(with_keywords=keyword_id, page=page)
            for item in response["results"]:
                if media == "movies":
                    xml += get_movie_xml(item)
                    content = "movies"
                elif media == "shows":
                    xml += get_show_xml(item)
                    content = "tvshows"
        elif url.startswith("collection"):
            split_url = url.split("/")
            collection_id = split_url[-1]
            if not response:
                response = tmdbsimple.Collections(collection_id).info()
            for item in response["parts"]:
                xml += get_movie_xml(item)
                content = "movies"
        elif url.startswith("search"):
            if url == "search":
                term = koding.Keyboard("Search For")
                url = "search/%s" % term
            split_url = url.split("/")
            if len(split_url) == 2:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            term = split_url[-2]
            response = tmdbsimple.Search().multi(query=term, page=page)
            for item in response["results"]:
                if item["media_type"] == "movie":
                    xml += get_movie_xml(item)
                elif item["media_type"] == "tv":
                    xml += get_show_xml(item)
                elif item["media_type"] == "person":
                    name = item["name"]
                    person_id = item["id"]
                    if item.get("profile_path", ""):
                        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["profile_path"]
                    else:
                        thumbnail = ""
                    if not COLOR1 == "" and not COLOR2 == "":
                        name = "[COLOR %s]%s [COLOR %s]Shows TMDB[/COLOR]" % (COLOR2, name.capitalize(), COLOR1)
                    else:
                        name = "%s Shows TMDB" % name.capitalize()
                    xml += "<dir>\n"\
                           "\t<title>%s</title>\n"\
                           "\t<tmdb>person/shows/%s</tmdb>\n"\
                           "\t<thumbnail>%s</thumbnail>\n"\
                           "</dir>\n\n" % (name, person_id, thumbnail)
                    if not COLOR1 == "" and not COLOR2 == "":
                        name = "[COLOR %s]%s [COLOR %s]Movies TMDB[/COLOR]" % (COLOR2, name.capitalize(), COLOR1)
                    else:
                        name = "%s Movies TMDB" % name.capitalize()
                    xml += "<dir>\n"\
                           "\t<title>%s</title>\n"\
                           "\t<tmdb>person/movies/%s</tmdb>\n"\
                           "\t<thumbnail>%s</thumbnail>\n"\
                           "\t</dir>\n\n" % (name, person_id, thumbnail)
        if response and page < response.get("total_pages", 0):
            base = url.split("/")
            if base[-1].isdigit():
                base = base[:-1]
            next_url = "/".join(base) + "/" + str(page + 1)
            if not COLOR2 == "":
                myPage = "[COLOR %s]Next Page >>[/COLOR]" % COLOR2
            else:
                myPage = "Next Page >>"
            xml += "<dir>"\
                   "<title>%s</title>"\
                   "<tmdb>%s</tmdb>"\
                   "<thumbnail>https://i.imgur.com/NuF4AN0.png</thumbnail>"\
                   "<summary>Go To Page %s</summary>"\
                   "</dir>" % (myPage, next_url, page + 1)
        __builtin__.content_type = content
        save_to_db((xml, __builtin__.content_type), url)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), __builtin__.content_type, pins)


def get_movie_xml(item):
    title = remove_non_ascii(item["title"])
    tmdb_id = item["id"]
    if "release_date" not in item:
        year = ""
    else:
        year = item["release_date"].split("-")[0]
        if not year:
            year = tmdbsimple.Movies(tmdb_id).info()["release_date"]
    url = "tmdb_imdb({0})".format(tmdb_id)
    imdb = fetch_from_db(url)
    if not imdb:
        imdb = item.get("imdb_id", "")
        if not imdb:
            imdb = tmdbsimple.Movies(tmdb_id).info()["imdb_id"]
        save_to_db(imdb, url)
    if item["poster_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["poster_path"]
    else:
        thumbnail = ""
    if item.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    name = title + " (" + year + ")"
    if not COLOR1 == "":
        name = "[COLOR %s]%s[/COLOR]" % (COLOR1, name)
    xml = "<item>"\
          "<title>%s</title>"\
          "<meta>"\
          "<imdb>%s</imdb>"\
          "<content>movie</content>"\
          "<title>%s</title>"\
          "<year>%s</year>"\
          "</meta>"\
          "<link>"\
          "<sublink>search</sublink>"\
          "<sublink>searchsd</sublink>"\
          "</link>"\
          "<thumbnail>%s</thumbnail>"\
          "<fanart>%s</fanart>"\
          "</item>" % (name, imdb, title, year, thumbnail, fanart)
    return xml


def get_trailer_xml(item):
    title = remove_non_ascii(item["title"])
    tmdb_id = item["id"]
    if "release_date" not in item:
        year = ""
    else:
        year = item["release_date"].split("-")[0]
        if not year:
            year = tmdbsimple.Movies(tmdb_id).info()["release_date"]
    # url = "tmdb_imdb({0})".format(tmdb_id)
    summary = remove_non_ascii(item["overview"])
    if item["poster_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["poster_path"]
    else:
        thumbnail = ""
    if item["backdrop_path"]:
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    name = title + " (" + year + ")"
    if not COLOR1 == "":
        name = "[COLOR %s]%s[/COLOR]" % (COLOR1, name)
    xml = "<dir>"\
          "<title>%s</title>"\
          "<tmdb>trailer/%s</tmdb>"\
          "<thumbnail>%s</thumbnail>"\
          "<fanart>%s</fanart>"\
          "<summary>%s</summary>"\
          "</dir>" % (name, tmdb_id, thumbnail, fanart, summary)
    return xml


def get_trailer_video_xml(item):
    title = remove_non_ascii(item["name"])
    # tmdb_id = item["id"]
    key = item["key"]
    # url = "tmdb_imdb({0})".format(tmdb_id)
    if not COLOR1 == "":
        title = "[COLOR %s]%s[/COLOR]" % (COLOR1, title)
    xml = "<item>"\
          "<title>%s</title>"\
          "<link>https://www.youtube.com/watch?v=%s&feature=youtube</link>"\
          "<summary>%s</summary>"\
          "</item>" % (title, key, title)
    return xml


def get_person_xml(item):
    title = remove_non_ascii(item["name"])
    tmdb_id = item["id"]
    # url = "tmdb_imdb({0})".format(tmdb_id)
    if item["profile_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["profile_path"]
    else:
        thumbnail = ""
    if item["profile_path"]:
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["profile_path"]
    else:
        fanart = ""
    if not COLOR1 == "":
        title = "[COLOR %s]%s[/COLOR]" % (COLOR1, title)
    xml = "<dir>"\
          "<title>%s</title>"\
          "<tmdb>person/movies/%s</tmdb>"\
          "<thumbnail>%s</thumbnail>"\
          "<fanart>%s</fanart>"\
          "<summary>%s</summary>"\
          "</dir>" % (title, tmdb_id, thumbnail, fanart, title)
    return xml


def get_show_xml(item):
    title = remove_non_ascii(item["name"])
    year = item["first_air_date"].split("-")[0]
    tmdb_id = item["id"]
    if item["poster_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["poster_path"]
    else:
        thumbnail = ""
    if item.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    if tmdb_id:
        url = "tmdb_imdb({0})".format(tmdb_id)
        imdb = fetch_from_db(url)
        if not imdb:
            try:
                imdb = tmdbsimple.TV(tmdb_id).external_ids()['imdb_id']
                save_to_db(imdb, url)
            except KeyError:
                imdb = "0"
    else:
        imdb = "0"
    name = title + " (" + year + ")"
    if not COLOR1 == "":
        name = "[COLOR %s]%s[/COLOR]" % (COLOR1, name)
    xml = "<dir>"\
          "<title>%s</title>"\
          "<meta>"\
          "<imdb>%s</imdb>"\
          "<content>tvshow</content>"\
          "<tvshowtitle>%s</tvshowtitle>"\
          "<year>%s</year>"\
          "</meta>"\
          "<link>tmdb_tv_show(%s, %s, %s)</link>"\
          "<thumbnail>%s</thumbnail>"\
          "<fanart>%s</fanart>"\
          "</dir>" % (name, imdb, title, year, tmdb_id, year, title,
                      thumbnail, fanart)
    return xml


def get_season_xml(item, tmdb_id, year, tvtitle):
    season = item["season_number"]
    if item["poster_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["poster_path"]
    else:
        thumbnail = ""
    if item.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    if tmdb_id:
        url = "tmdb_imdb({0})".format(tmdb_id)
        imdb = fetch_from_db(url)
        if not imdb:
            imdb = tmdbsimple.TV(tmdb_id).external_ids()['imdb_id']
            save_to_db(imdb, url)
    else:
        imdb = "0"
    if not COLOR1 == "" and not COLOR2 == "":
        name = "[COLOR %s]Season: [COLOR %s]%s[/COLOR]" % (COLOR1, COLOR2, season)
    else:
        name = "Season: %s" % (season)
    xml = "<dir>"\
          "<title>%s</title>"\
          "<meta>"\
          "<imdb>%s</imdb>"\
          "<content>season</content>"\
          "<season>%s</season>"\
          "</meta>"\
          "<thumbnail>%s</thumbnail>"\
          "<fanart>%s</fanart>"\
          "<link>tmdb_season(%s,%s, %s, %s)</link>"\
          "</dir>" % (name, imdb, season, thumbnail, fanart, tmdb_id,
                      season, year, tvtitle)
    return xml


def get_episode_xml(item, tmdb_id, year, tvtitle):
    title = remove_non_ascii(item["name"])
    season = item["season_number"]
    episode = item["episode_number"]
    if tmdb_id:
        url = "tmdb_imdb({0})".format(tmdb_id)
        imdb = fetch_from_db(url)
        if not imdb:
            imdb = tmdbsimple.TV(tmdb_id).external_ids()['imdb_id']
            save_to_db(imdb, url)
    else:
        imdb = "0"
    premiered = item["air_date"]
    if item["still_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["still_path"]
    else:
        thumbnail = ""
    if item.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    if int(season) > 0 and int(season) < 10:
        mySeason = "0" + str(season)
    else:
        mySeason = str(season)
    if int(episode) > 0 and int(episode) < 10:
        myEpisode = "0" + str(episode)
    else:
        myEpisode = str(episode)
    if not COLOR1 == "" and not COLOR2 == "":
        name = "[COLOR %s]S%sE%s[/COLOR] - [COLOR %s]%s[/COLOR]" % (COLOR2, mySeason, myEpisode, COLOR1, title)
    else:
        name = "S%sE%s - %s" % (mySeason, myEpisode, title)
    xml = "<item>"\
          "<title>%s</title>"\
          "<meta>"\
          "<imdb>%s</imdb>"\
          "<content>episode</content>"\
          "<tvshowtitle>%s</tvshowtitle>"\
          "<year>%s</year>"\
          "<title>%s</title>"\
          "<premiered>%s</premiered>"\
          "<season>%s</season>"\
          "<episode>%s</episode>"\
          "</meta>"\
          "<link>"\
          "<sublink>search</sublink>"\
          "<sublink>searchsd</sublink>"\
          "</link>"\
          "<thumbnail>%s</thumbnail>"\
          "<fanart>%s</fanart>"\
          "</item>" % (name, imdb, tvtitle, year, title,
                       premiered, season, episode, thumbnail, fanart)
    return xml


@route(mode='tmdb_tv_show', args=["url"])
def tmdb_tv_show(url):
    pins = ""
    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        splitted = url.replace("tmdb_id", "").split(",")
        tmdb_id = splitted[0]
        year = splitted[1]
        tvtitle = ",".join(splitted[2:])
        response = tmdbsimple.TV(tmdb_id).info()
        seasons = response["seasons"]
        xml = ""
        for season in seasons:
            xml += get_season_xml(season, tmdb_id, year, tvtitle)
        save_to_db(xml, url)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='tmdb_season', args=["url"])
def tmdb_season(url):
    pins = ""
    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        splitted = url.replace("tmdb_id", "").split(",")
        tmdb_id = splitted[0]
        season = splitted[1]
        year = splitted[2]
        tvtitle = ",".join(splitted[3:])
        response = tmdbsimple.TV_Seasons(tmdb_id, season).info()
        episodes = response["episodes"]
        xml = ""
        for episode in episodes:
            xml += get_episode_xml(episode, tmdb_id, year, tvtitle)
        save_to_db(xml, url)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def remove_non_ascii(text):
    return unidecode(text)


def save_to_db(item, url):
    if not item or not url:
        return False
    koding.reset_db()
    koding.Remove_From_Table(
        "tmdb_plugin",
        {
            "url": url
        })

    koding.Add_To_Table("tmdb_plugin",
                        {
                            "url": url,
                            "item": base64.b64encode(pickle.dumps(item)),
                            "created": time.time()
                        })


def fetch_from_db(url):
    koding.reset_db()
    tmdb_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("tmdb_plugin", tmdb_plugin_spec)
    match = koding.Get_From_Table(
        "tmdb_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if created_time and float(created_time) + CACHE_TIME >= time.time():
            match_item = match["item"]
            try:
                    result = pickle.loads(base64.b64decode(match_item))
            except:
                    return None
            return result
        else:
            return []
    else:
        return []