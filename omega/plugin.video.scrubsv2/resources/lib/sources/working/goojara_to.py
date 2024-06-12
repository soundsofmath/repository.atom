# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import scrape_sources
from resources.lib.modules import search_engines
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        self.results = []
        self.domains = ['goojara.to', 'supernova.to']
        self.base_link = 'https://goojara.to'


    def movie(self, imdb, tmdb, title, localtitle, aliases, year):
        url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
        url = urlencode(url)
        return url


    def tvshow(self, imdb, tmdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        url = {'imdb': imdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
        url = urlencode(url)
        return url


    def episode(self, url, imdb, tmdb, tvdb, title, premiered, season, episode):
        if not url:
            return
        url = parse_qs(url)
        url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
        url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
        url = urlencode(url)
        return url


    def sources(self, url, hostDict):
        try:
            if not url:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            if 'tvshowtitle' in data:
                search_query = search_engines.make_search_query(self.domains[0], title, season=season, episode=episode, domainprefix='')
                check_title = 'Watch+%s+Season+%s+Episode+%s' % (title, season, episode)
            else:
                search_query = search_engines.make_search_query(self.domains[0], title, year=year, domainprefix='')
                check_title = 'Watch+%s+(%s)' % (title, year)
            check_title = cleantitle.get_plus(check_title)
            results = search_engines.bing(search_query, parse=True)
            result_url = [i[0] for i in results if check_title in cleantitle.get_plus(i[1]) and self.domains[0] in i[0]][0]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            result_html = client.request(result_url, headers=headers, output='extended')
            result_links = re.compile('<a class="bcg" href="(.+?)">(.+?)<span>', re.DOTALL).findall(result_html[0])
            cookie_code = re.compile("\('(.+?)','(.+?)'\);", re.DOTALL).findall(result_html[0])
            cookies = ["%s=%s" % (key, value) for key, value in cookie_code]
            cookies += [result_html[3]]
            cookies = '; '.join([i for i in cookies])
            hosters = []
            for link, hoster in result_links:
                try:
                    if scrape_sources.check_host_limit(hoster, hosters):
                        continue
                    else:
                        hosters.append(hoster)
                    link = client.request(link, headers=result_html[1], cookie=cookies, output='geturl')
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
                except:
                    #log_utils.log('sources', 1)
                    pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


