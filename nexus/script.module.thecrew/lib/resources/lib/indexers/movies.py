# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    -Mofidied by The Crew
    -Copyright (C) 2019 The Crew


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from resources.lib.modules import trakt
from resources.lib.modules import cleangenre
from resources.lib.modules import cleantitle
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.modules import log_utils
from resources.lib.indexers import navigator

import os,sys,re,datetime,base64,traceback
import simplejson as json

import six
from six.moves import urllib_parse, zip, range

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database


params = dict(urllib_parse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')

class movies:
    def __init__(self):
        self.count = int(control.setting('page.item.limit'))
        self.list = []

        self.imdb_link = 'https://www.imdb.com'
        self.trakt_link = 'https://api.trakt.tv'
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.year_date = (self.datetime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tm_user = control.setting('tm.user')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))
        self.lang = control.apiLanguage()['trakt']

        self.hidecinema = control.setting('hidecinema')
        self.hidecinema_rollback = int(control.setting('hidecinema.rollback'))
        self.hidecinema_rollback2 = self.hidecinema_rollback * 30
        self.hidecinema_date = (datetime.date.today() - datetime.timedelta(days=self.hidecinema_rollback2)).strftime('%Y-%m')

        self.search_link = 'https://api.trakt.tv/search/movie?limit=20&page=1&query='
        self.fanart_tv_art_link = 'https://webservice.fanart.tv/v3/movies/%s'
        self.fanart_tv_level_link = 'https://webservice.fanart.tv/v3/level'
        self.tm_art_link = 'https://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % ('%s', self.tm_user, self.lang)
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'

        self.persons_link = 'https://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'https://www.imdb.com/search/name?count=100&gender=male,female'
        self.person_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&role=%s&sort=year,desc&count=%d&start=1' % ('%s', self.count)
        self.keyword_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&keywords=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
        self.oscars_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=%d&start=1' % self.count
        self.oscarsnominees_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_nominees&sort=year,desc&count=%d&start=1' % self.count
        self.theaters_link = 'https://www.imdb.com/search/title?title_type=feature&num_votes=1000,&release_date=date[365],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.year_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', '%s', self.count)

        if self.hidecinema == 'true':
            self.popular_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&release_date=,%s&sort=moviemeter,asc&count=%d&start=1' % (self.hidecinema_date, self.count)
            self.views_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=,%s&sort=num_votes,desc&count=%d&start=1' % (self.hidecinema_date, self.count)
            self.featured_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=,%s&sort=moviemeter,asc&count=%d&start=1' % (self.hidecinema_date, self.count)
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,%s&genres=%s&sort=moviemeter,asc&count=%d&start=1' % (self.hidecinema_date, '%s', self.count)
            self.language_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&release_date=,%s&count=%d&start=1' % ('%s', self.hidecinema_date, self.count)
            self.certification_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=%s&sort=moviemeter,asc&release_date=,%s&count=%d&start=1' % ('%s', self.hidecinema_date, self.count)
            self.boxoffice_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&release_date=,%s&count=%d&start=1' % (self.hidecinema_date, self.count)
        else:
            self.popular_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=%d&start=1' % self.count
            self.views_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=%d&start=1' % self.count
            self.featured_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=moviemeter,asc&count=%d&start=1' % self.count
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
            self.language_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
            self.certification_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
            self.boxoffice_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&count=%d&start=1' % self.count

        self.top100_link = 'https://www.imdb.com/search/title?title_type=feature&groups=top_100&count=%d&start=1' % self.count
        self.top250_link = 'https://www.imdb.com/search/title?title_type=feature&groups=top_250&count=%d&start=1' % self.count
        self.top1000_link = 'https://www.imdb.com/search/title?title_type=feature&groups=top_1000&count=%d&start=1' % self.count
        self.rated_g_link = 'https://www.imdb.com/search/title/?certificates=US%3AG'
        self.rated_pg13_link = 'https://www.imdb.com/search/title/?certificates=US%3APG-13'
        self.rated_pg_link = 'https://www.imdb.com/search/title/?certificates=US%3APG'
        self.rated_r_link = 'https://www.imdb.com/search/title/?certificates=US%3AR'
        self.rated_nc17_link = 'https://www.imdb.com/search/title/?certificates=US%3ANC-17'
        self.bestdirector_link = 'https://www.imdb.com/search/title?title_type=feature&groups=best_director_winner&sort=user_rating,desc&count=%d&start=1' % self.count
        self.national_film_board_link = 'https://www.imdb.com/search/title?title_type=feature&groups=national_film_preservation_board_winner&sort=user_rating,desc&count=%d&start=1' % self.count
        self.dreamworks_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=dreamworks&count=%d&start=1' % self.count
        self.fox_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=fox&count=%d&start=1' % self.count
        self.paramount_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=paramount&count=%d&start=1' % self.count
        self.mgm_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=mgm&count=%d&start=1' % self.count
        self.universal_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=universal&count=%d&start=1' % self.count
        self.sony_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=sony&count=%d&start=1' % self.count
        self.warnerbrothers_pictures = 'https://www.imdb.com/search/title?title_type=feature&companies=warner&count=%d&start=1' % self.count
        self.amazon_prime_link = 'https://www.imdb.com/search/title?title_type=feature&online_availability=US%2Ftoday%2FAmazon%2Fsubs'
        self.disney_pictures_link = 'https://www.imdb.com/search/title?user_rating=1.0,10.0&companies=disney&count=%d&start=1' % self.count
        self.family_movies_link = 'https://www.imdb.com/search/title/?title_type=feature&genres=family&count=%d&start=1' % self.count
        self.classic_movies_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&count=%d&start=1' % self.count
        self.classic_horror_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=horror&count=%d&start=1' % self.count
        self.classic_fantasy_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=fantasy&count=%d&start=1' % self.count
        self.classic_western_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=western&count=%d&start=1' % self.count
        self.classic_annimation_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=animation&count=%d&start=1' % self.count
        self.classic_war_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=war&count=%d&start=1' % self.count
        self.classic_scifi_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=sci_fi&count=%d&start=1' % self.count
        self.eighties_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1980-01-01,1989-12-31&count=%d&start=1' % self.count
        self.nineties_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1990-01-01,1999-12-31&count=%d&start=1' % self.count
        self.thousands_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2010-12-31&count=%d&start=1' % self.count
        self.twentyten_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=2010-01-01,2019-12-31&count=%d&start=1' % self.count
        self.advancedsearchtrending_link = 'https://www.imdb.com/search/title?title_type=feature&genres=animation,family&sort=moviemeter,asc&page=1&ref_=adv_prv'
        self.collectionsactionhero_link = 'https://www.imdb.com/search/keyword/?keywords=action-hero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=7846868c-8414-4178-8f43-9ad6b2ef0baf&pf_rd_r=N2RAG179F05MS9C7TEF4&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=moka&ref_=kw_1&sort=num_votes,desc&mode=detail&page=1'
        self.advancedsearchdcvsmarvel_link = 'https://www.imdb.com/list/ls065237713/?sort=alpha,asc&st_dt=&mode=detail&page=1'

        self.added_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&languages=en&num_votes=500,&production_status=released&release_date=%s,%s&sort=release_date,desc&count=20&start=1' % (self.year_date, self.today_date)
        self.trending_link = 'https://api.trakt.tv/movies/trending?limit=%d&page=1' % self.count
        self.traktlists_link = 'https://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'https://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'https://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'https://api.trakt.tv/users/me/collection/movies'
        self.traktwatchlist_link = 'https://api.trakt.tv/users/me/watchlist/movies'
        self.traktfeatured_link = 'https://api.trakt.tv/recommendations/movies?limit=%d' % self.count
        self.trakthistory_link = 'https://api.trakt.tv/users/me/history/movies?limit=%d&page=1' % self.count
        self.onDeck_link = 'https://api.trakt.tv/sync/playback/movies?extended=full&limit=%d' % self.count
        self.imdblists_link = 'https://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'https://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=movie,short,tvMovie,tvSpecial,video&start=1'
        self.imdblist2_link = 'https://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=movie,short,tvMovie,tvSpecial,video&start=1'
        self.imdbwatchlist_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user

#######HALLOWEEN########
        self.halloween_imdb_link = 'https://www.imdb.com/list/ls066334100/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count
        self.halloween_top_100_link = 'https://www.imdb.com/list/ls000091321/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count
        self.halloween_best_link = 'https://www.imdb.com/list/ls052042029/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count
        self.halloween_great_link = 'https://www.imdb.com/list/ls050722485/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count

#######HOLIDAY########
        self.top50_holiday_link = 'https://www.imdb.com/list/ls003988974/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count
        self.best_holiday_link = 'https://www.imdb.com/list/ls053245198/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count

    def get(self, url, idx=True, create_directory=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass

            try:
                u = urllib_parse.urlparse(url).netloc.lower()
            except:
                pass

            if self.trakt_link in url and url == self.onDeck_link:
                self.blist = cache.get(self.trakt_list, 720, url, self.trakt_user)
                self.list = []
                self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)
                self.list = self.list[::-1]

                if idx == True:
                    self.worker()

            elif u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakthistory_link:
                        raise Exception()
                    if not '/users/me/' in url:
                        raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user):
                        raise Exception()
                    self.list = cache.get(
                        self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)

                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))

                if idx == True:
                    self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True:
                    self.worker(level=0)

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True:
                    self.worker()

            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True:
                    self.worker()

            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True:
                    self.worker()

            if idx == True and create_directory == True:
                self.movieDirectory(self.list)
            return self.list
        except:
            pass

    def widget(self):
        setting = control.setting('movie.widget')

        if setting == '2':
            self.get(self.trending_link)
        elif setting == '3':
            self.get(self.popular_link)
        elif setting == '4':
            self.get(self.theaters_link)
        elif setting == '5':
            self.get(self.added_link)
        else:
            self.get(self.featured_link)


    def search(self):
        navigator.navigator().addDirectoryItem(32603, 'movieSearchnew', 'search.png', 'DefaultMovies.png')
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()

        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS movies (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except:
            pass

        dbcur.execute("SELECT * FROM movies ORDER BY ID DESC")
        lst = []

        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.navigator().addDirectoryItem(term, 'movieSearchterm&name=%s' % term, 'search.png', 'DefaultMovies.png')
                lst += [(term)]
        dbcur.close()

        if delete_option:
            navigator.navigator().addDirectoryItem(32605, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')

        navigator.navigator().endDirectory()

    def search_new(self):
        t = six.ensure_str(control.lang(32010))
        k = control.keyboard('', t)
        k.doModal()
        q = k.getText() if k.isConfirmed() else None

        if (q is None or q == ''): return

        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("INSERT INTO movies VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.search_link + urllib_parse.quote_plus(q)
        self.get(url)

    def search_term(self, name):
        url = self.search_link + urllib_parse.quote_plus(name)
        self.get(url)

    def person(self):
        try:
            t = six.ensure_str(control.lang(32010))
            k = control.keyboard('', t)
            k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''): return

            url = self.persons_link + urllib_parse.quote_plus(q)
            self.persons(url)
        except:
            return


# TC 2/01/19 started
    def genres(self):
        genres = [
            ('Action', 'action', True),
            ('Adventure', 'adventure', True),
            ('Animation', 'animation', True),
            ('Anime', 'anime', False),
            ('Biography', 'biography', True),
            ('Comedy', 'comedy', True),
            ('Crime', 'crime', True),
            ('Documentary', 'documentary', True),
            ('Drama', 'drama', True),
            ('Family', 'family', True),
            ('Fantasy', 'fantasy', True),
            ('History', 'history', True),
            ('Horror', 'horror', True),
            ('Music ', 'music', True),
            ('Musical', 'musical', True),
            ('Mystery', 'mystery', True),
            ('Romance', 'romance', True),
            ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True),
            ('Thriller', 'thriller', True),
            ('War', 'war', True),
            ('Western', 'western', True)
        ]

        for i in genres:
            self.list.append(
                {
                    'name': cleangenre.lang(i[0], self.lang),
                    'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                    'image': 'genres.png',
                    'action': 'movies'
                })

        self.addDirectory(self.list)
        return self.list

    def languages(self):
        languages = [
            ('Arabic', 'ar'),
            ('Bosnian', 'bs'),
            ('Bulgarian', 'bg'),
            ('Chinese', 'zh'),
            ('Croatian', 'hr'),
            ('Dutch', 'nl'),
            ('English', 'en'),
            ('Finnish', 'fi'),
            ('French', 'fr'),
            ('German', 'de'),
            ('Greek', 'el'),
            ('Hebrew', 'he'),
            ('Hindi ', 'hi'),
            ('Hungarian', 'hu'),
            ('Icelandic', 'is'),
            ('Italian', 'it'),
            ('Japanese', 'ja'),
            ('Korean', 'ko'),
            ('Macedonian', 'mk'),
            ('Norwegian', 'no'),
            ('Persian', 'fa'),
            ('Polish', 'pl'),
            ('Portuguese', 'pt'),
            ('Punjabi', 'pa'),
            ('Romanian', 'ro'),
            ('Russian', 'ru'),
            ('Serbian', 'sr'),
            ('Slovenian', 'sl'),
            ('Spanish', 'es'),
            ('Swedish', 'sv'),
            ('Turkish', 'tr'),
            ('Ukrainian', 'uk')
        ]

        for i in languages:
            self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'international.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def certifications(self):
        certificates = ['[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]G[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]', '[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]PG[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]',
                        '[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]PG-13[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]', '[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]R[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]', '[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]NC-17[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]']

        for i in certificates:
            self.list.append({'name': str(i), 'url': self.certification_link % str(i).replace('-', '_').lower(), 'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def years(self):
        year = (self.datetime.strftime('%Y'))

        for i in list(range(int(year)-0, 1900, -1)):
            self.list.append({'name': str(i), 'url': self.year_link % (str(i), str(i)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in list(range(0, len(self.list))):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '':
                raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass

        self.list = userlists
        for i in list(range(0, len(self.list))):
            self.list[i].update({'image': 'userlists.png', 'action': 'movies'})
        self.addDirectory(self.list, queue=True)
        return self.list

    def trakt_list(self, url, user):
        try:
            q = dict(urllib_parse.parse_qsl(urllib_parse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib_parse.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urllib_parse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)
            result = control.six_decode(result)

            items = []
            for i in result:
                try:
                    items.append(i['movie'])
                except:
                    pass
            if len(items) == 0:
                items = result
        except:
            return

        try:
            q = dict(urllib_parse.parse_qsl(urllib_parse.urlsplit(url).query))
            if not int(q['limit']) == len(items):
                raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib_parse.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urllib_parse.urlparse(url).query, '') + '?' + q
            next = six.ensure_str(next)
        except:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)

                year = item['year']
                year = re.sub(r'[^0-9]', '', str(year))

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    raise Exception()
                imdb = 'tt' + re.sub(r'[^0-9]', '', str(imdb))

                tmdb = str(item.get('ids', {}).get('tmdb', 0))

                try:
                    premiered = item['released']
                except:
                    premiered = '0'
                try:
                    premiered = re.compile(
                        r'(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'

                try:
                    genre = item['genres']
                except:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)

                try:
                    duration = str(item['runtime'])
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'

                try:
                    rating = str(item['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'

                try:
                    votes = str(item['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes), ',d'))
                except:
                    pass
                if not votes: votes = '0'

                try:
                    mpaa = item['certification']
                except:
                    mpaa = '0'
                if not mpaa: mpaa = '0'

                try:
                    plot = item['overview']
                except:
                    plot = '0'
                if not plot: plot = '0'
                plot = client.replaceHTMLCodes(plot)

                try:
                    tagline = item['tagline']
                except:
                    tagline = '0'
                if tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'genre': genre, 'duration': duration, 'rating': rating,
                                  'votes': votes, 'mpaa': mpaa, 'plot': plot, 'tagline': tagline, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': '0', 'next': next})
            except:
                pass

        return self.list

    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            pass

        for item in items:
            try:
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client.replaceHTMLCodes(name)

                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

    def imdb_list(self, url):
        try:
            for i in re.findall(r'date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs={'property': 'pageId'})[0]

            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url

            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url

            result = client.request(url)
            result = control.six_decode(result)

            result = result.replace('\n', ' ')

            items = client.parseDOM(result, 'div', attrs={'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs={'class': 'list_item.+?'})
        except:
            return

        try:
            next = client.parseDOM(result, 'a', ret='href', attrs={'class': '.+?ister-page-nex.+?'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs={'class': 'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'),client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urllib_parse.urlparse(url).query, urllib_parse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = six.ensure_str(next)
        except:
            next = ''

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = six.ensure_str(title)

                year = client.parseDOM(item, 'span', attrs={'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs={'class': 'year_type'})
                try:
                    year = re.compile(r'(\d{4})').findall(year)[0]
                except:
                    year = '0'
                year = six.ensure_str(year)

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall(r'(tt\d*)', imdb)[0]

                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    poster = '0'
                if '/nopicture/' in poster:
                    poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = six.ensure_str(poster)

                try:
                    genre = client.parseDOM(item, 'span', attrs={'class': 'genre'})[0]
                except:
                    genre = '0'
                genre = ' / '.join([i.strip() for i in genre.split(',')])
                if genre == '':
                    genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = six.ensure_str(genre)

                try:
                    duration = re.findall(r'(\d+?) min(?:s|)', item)[-1]
                except:
                    duration = '0'
                duration = six.ensure_str(duration)

                rating = '0'
                try:
                    rating = client.parseDOM(item, 'span', attrs={'class': 'rating-rating'})[0]
                except:
                    pass
                try:
                    rating = client.parseDOM(rating, 'span', attrs={'class': 'value'})[0]
                except:
                    rating = '0'
                try:
                    rating = client.parseDOM(item, 'div', ret='data-value', attrs={'class': '.*?imdb-rating'})[0]
                except:
                    pass
                if rating == '' or rating == '-':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)

                try:
                    votes = client.parseDOM(item, 'div', ret='title', attrs={'class': '.*?rating-list'})[0]
                except:
                    votes = '0'
                try:
                    votes = re.findall('\((.+?) vote(?:s|)\)', votes)[0]
                except:
                    votes = '0'
                if not votes: votes = '0'
                votes = client.replaceHTMLCodes(votes)

                try:
                    mpaa = client.parseDOM(item, 'span', attrs={'class': 'certificate'})[0]
                except:
                    mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED':
                    mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)

                try:
                    director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    director = '0'
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '':
                    director = '0'
                director = client.replaceHTMLCodes(director)

                try:
                    cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    cast = '0'
                cast = client.replaceHTMLCodes(cast)
                cast = six.ensure_str(cast)
                cast = client.parseDOM(cast, 'a')
                if cast == []:
                    cast = '0'

                plot = '0'
                try:
                    plot = client.parseDOM(item, 'p', attrs={'class': 'text-muted'})[0]
                except:
                    pass
                try:
                    plot = client.parseDOM(item, 'div', attrs={'class': 'item_description'})[0]
                except:
                    pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                plot = re.sub(r'<.+?>|</.+?>', '', plot)
                if plot == '':
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = six.ensure_str(plot)

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa,
                                  'director': director, 'cast': cast, 'plot': plot, 'tagline': '0', 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass

        return self.list

    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs={'class': '.+?etail'})
        except:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = six.ensure_str(name)

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall(r'(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)

                image = client.parseDOM(item, 'img', ret='src')[0]
                # if not ('._SX' in image or '._SY' in image): raise Exception()
                image = re.sub(r'(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            result = control.six_decode(result)
            items = client.parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = six.ensure_str(name)

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

    def worker(self, level=1):
        self.meta = []
        total = len(self.list)

        self.fanart_tv_headers = {'api-key': '39b90a017e391afd33750f97827f8d96'}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

        for i in list(range(0, total)):
            self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in list(range(0, total, 40)):
            threads = []
            for i in list(range(r, r+40)):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.meta: metacache.insert(self.meta)

        self.list = [i for i in self.list if not i['imdb'] == '0']

        self.list = metacache.local(self.list, self.tm_img_link, 'poster3', 'fanart2')

        if self.fanart_tv_user == '':
            for i in self.list: i.update({'clearlogo': '0', 'clearart': '0'})

    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                raise Exception()

            imdb = self.list[i]['imdb']

            item = trakt.getMovieSummary(imdb)
            item = control.six_decode(item)

            title = item.get('title')
            title = client.replaceHTMLCodes(title)

            originaltitle = title

            year = item.get('year', 0)
            year = re.sub(r'[^0-9]', '', str(year))

            imdb = item.get('ids', {}).get('imdb', '0')
            imdb = 'tt' + re.sub(r'[^0-9]', '', str(imdb))

            tmdb = str(item.get('ids', {}).get('tmdb', 0))

            premiered = item.get('released', '0')
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except:
                premiered = '0'

            genre = item.get('genres', [])
            genre = [x.title() for x in genre]
            genre = ' / '.join(genre).strip()
            if not genre: genre = '0'

            duration = str(item.get('Runtime', 0))

            rating = item.get('rating', '0')
            if not rating or rating == '0.0':
                rating = '0'

            votes = item.get('votes', '0')
            try:
                votes = str(format(int(votes), ',d'))
            except:
                pass

            mpaa = item.get('certification', '0')
            if not mpaa: mpaa = '0'

            tagline = item.get('tagline', '0')

            plot = item.get('overview', '0')

            people = trakt.getPeople(imdb, 'movies')

            director = writer = ''
            if 'crew' in people and 'directing' in people['crew']:
                director = ', '.join([director['person']['name'] for director in people['crew']['directing'] if director['job'].lower() == 'director'])
            if 'crew' in people and 'writing' in people['crew']:
                writer = ', '.join([writer['person']['name'] for writer in people['crew']['writing'] if writer['job'].lower() in ['writer', 'screenplay', 'author']])

            cast = []
            for person in people.get('cast', []): cast.append({'name': person['person']['name'], 'role': person['character']})
            cast = [(person['name'], person['role']) for person in cast]

            try:
                if self.lang == 'en' or self.lang not in item.get('available_translations', [self.lang]):
                    raise Exception()

                trans_item = trakt.getMovieTranslation(imdb, self.lang, full=True)

                title = trans_item.get('title') or title
                tagline = trans_item.get('tagline') or tagline
                plot = trans_item.get('overview') or plot
            except:
                pass

            try:
                artmeta = True
                art = client.request(self.fanart_tv_art_link % imdb, headers=self.fanart_tv_headers, timeout='10', error=True)
                try:
                    art = json.loads(art)
                except:
                    artmeta = False
            except:
                pass

            try:
                poster2 = art['movieposter']
                poster2 = [x for x in poster2 if x.get('lang') == self.lang][::-1] + [x for x in poster2 if x.get('lang') == 'en'][::-1] + [x for x in poster2 if x.get('lang') in ['00', '']][::-1]
                poster2 = six.ensure_str(poster2[0]['url'])
            except:
                poster2 = '0'

            try:
                if 'moviebackground' in art:
                    fanart = art['moviebackground']
                else:
                    fanart = art['moviethumb']
                fanart = [x for x in fanart if x.get('lang') == self.lang][::-1] + [x for x in fanart if x.get('lang') == 'en'][::-1] + [x for x in fanart if x.get('lang') in ['00', '']][::-1]
                fanart = six.ensure_str(fanart[0]['url'])
            except:
                fanart = '0'

            try:
                banner = art['moviebanner']
                banner = [x for x in banner if x.get('lang') == self.lang][::-1] + [x for x in banner if x.get('lang') == 'en'][::-1] + [x for x in banner if x.get('lang') in ['00', '']][::-1]
                banner = six.ensure_str(banner[0]['url'])
            except:
                banner = '0'

            try:
                if 'hdmovielogo' in art:
                    clearlogo = art['hdmovielogo']
                else:
                    clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == self.lang][::-1] + [x for x in clearlogo if x.get('lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = six.ensure_str(clearlogo[0]['url'])
            except:
                clearlogo = '0'

            try:
                if 'hdmovieclearart' in art:
                    clearart = art['hdmovieclearart']
                else:
                    clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == self.lang][::-1] + [x for x in clearart if x.get('lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = six.ensure_str(clearart[0]['url'])
            except:
                clearart = '0'

            try:
                if self.tm_user == '': raise Exception()

                art2 = client.request(self.tm_art_link % imdb, timeout='10', error=True)
                art2 = json.loads(art2)
            except:
                pass

            try:
                poster3 = art2['posters']
                poster3 = [x for x in poster3 if x.get('iso_639_1') == self.lang] + [x for x in poster3 if x.get('iso_639_1') == 'en'] + [x for x in poster3 if x.get('iso_639_1') not in [self.lang, 'en']]
                poster3 = [(x['width'], x['file_path']) for x in poster3]
                poster3 = [(x[0], x[1]) if x[0] < 300 else ('300', x[1]) for x in poster3]
                poster3 = self.tm_img_link % poster3[0]
                poster3 = six.ensure_str(poster3)
            except:
                poster3 = '0'

            try:
                fanart2 = art2['backdrops']
                fanart2 = [x for x in fanart2 if x.get('iso_639_1') == self.lang] + [x for x in fanart2 if x.get('iso_639_1') == 'en'] + [x for x in fanart2 if x.get('iso_639_1') not in [self.lang, 'en']]
                fanart2 = [x for x in fanart2 if x.get('width') == 1920] + [x for x in fanart2 if x.get('width') < 1920]
                fanart2 = [(x['width'], x['file_path']) for x in fanart2]
                fanart2 = [(x[0], x[1]) if x[0] < 1280 else ('1280', x[1]) for x in fanart2]
                fanart2 = self.tm_img_link % fanart2[0]
                fanart2 = six.ensure_str(fanart2)
            except:
                fanart2 = '0'

            item = {'title': title, 'originaltitle': originaltitle, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'poster': '0', 'poster2': poster2, 'poster3': poster3, 'banner': banner, 'fanart': fanart, 'fanart2': fanart2, 'clearlogo': clearlogo,
                    'clearart': clearart, 'premiered': premiered, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}
            item = dict((k,v) for k, v in six.iteritems(item) if not v == '0')
            self.list[i].update(item)

            if artmeta == False:
                raise Exception()

            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
        except:
            pass

    def movieDirectory(self, items):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()

        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        try:
            isOld = False
            control.item().getArt('type')
        except:
            isOld = True

        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'

        indicators = playcount.getMovieIndicators()

        playbackMenu = control.lang(32063) if control.setting('hosts.mode') == '2' else control.lang(32064)

        watchedMenu = control.lang(32068) if trakt.getTraktIndicatorsInfo() == True else control.lang(32066)

        unwatchedMenu = control.lang(32069) if trakt.getTraktIndicatorsInfo() == True else control.lang(32067)

        queueMenu = control.lang(32065)

        traktManagerMenu = control.lang(32070)

        nextMenu = control.lang(32053)

        addToLibrary = control.lang(32551)

        infoMenu = control.lang(32101)

        for i in items:
            try:
                label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                sysname = urllib_parse.quote_plus('%s (%s)' % (title, year))
                systitle = urllib_parse.quote_plus(title)

                meta = dict((k,v) for k, v in six.iteritems(i) if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib_parse.quote_plus(label))})
                #meta.update({'trailer': 'plugin://script.extendedinfo/?info=playtrailer&&id=%s' % imdb})
                if not 'duration' in i:
                    meta.update({'duration': '120'})
                elif i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass

                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})

                sysmeta = urllib_parse.quote_plus(json.dumps(meta))

                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib_parse.quote_plus(url)

                path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)

                cm = []
                cm.append(('Find similar', 'ActivateWindow(10025,%s?action=movies&url=https://api.trakt.tv/movies/%s/related,return)' % (sysaddon, imdb)))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' % (sysaddon, sysname, imdb)))

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if isOld == True:
                    cm.append((infoMenu, 'Action(Info)'))

                cm.append((addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, sysname, systitle, year, imdb, tmdb)))

                item = control.item(label=label)

                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})

                if settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    item.setProperty('Fanart_Image', i['fanart2'])
                elif settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels = control.metadataClean(meta))

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()

            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib_parse.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        queueMenu = control.lang(32065)

        playRandom = control.lang(32535)

        addToLibrary = control.lang(32551)

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib_parse.quote_plus(i['url'])
                except:
                    pass

                cm = []

                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=movie&url=%s)' % (sysaddon, urllib_parse.quote_plus(i['url']))))

                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=moviesToLibrary&url=%s)' % (sysaddon, urllib_parse.quote_plus(i['context']))))
                except:
                    pass

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
