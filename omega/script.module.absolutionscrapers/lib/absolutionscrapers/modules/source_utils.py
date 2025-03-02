# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    ///Updated for absolution///

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
"""

import base64
import hashlib
import re
from kodi_six import xbmc
import six
from six.moves import urllib_parse

from absolutionscrapers.modules import cleantitle
from absolutionscrapers.modules import client
from absolutionscrapers.modules import directstream
from absolutionscrapers.modules import log_utils
from absolutionscrapers.modules import trakt
from absolutionscrapers.modules import pyaes


RES_4K = ['.4k.', '.hd4k.', '.4khd.', '.uhd.', '.ultrahd.', '.ultra.hd.', '2160', '216o']
RES_1080 = ['1080', '1o8o', '.fullhd.', '.full.hd.', '.fhd.']
RES_720 = ['.720.', '.720p.', '.720i.', '.hd720.', '.720hd.', '.72o.', '.72op.']
RES_SD = ['576', '480', '.360.', '.360p.', '.360i.', '.sd360.', '.360sd.', '.240.', '.240p.', '.240i.', '.sd240.', '.240sd.']
SCR = ['.scr.', '.screener.', '.dvdscr.', '.dvd.scr.', '.r5.', '.r6.']
CAM = ['.camrip.', '.tsrip.', '.hdcam.', '.hd.cam.', '.cam.rip.', '.hdts.', '.dvdcam.', '.dvdts.', '.cam.', '.telesync.', '.ts.']
AVC = ['.h.264.', '.h264.', '.x264.', '.avc.']


def supported_video_extensions():
    supported_video_extensions = xbmc.getSupportedMedia('video').split('|')
    unsupported = ['', '.url', '.bin', '.zip', '.rar', '.001', '.disc', '.7z', '.tar.gz', '.tar.bz2',
                   '.tar.xz', '.tgz', '.tbz2', '.gz', '.bz2', '.xz', '.tar']
    return [i for i in supported_video_extensions if i not in unsupported]


def get_qual(term):
    term = '.{}.'.format(term).lower()
    if any(i in term for i in SCR):
        return 'scr'
    elif any(i in term for i in CAM):
        return 'cam'
    elif any(i in term for i in RES_4K) and not any(i in term for i in RES_1080):
        return '4k'
    elif any(i in term for i in RES_1080):
        return '1080p'
    elif any(i in term for i in RES_720):
        return '720p'
    elif any(i in term for i in RES_SD):
        return 'sd'
    elif 'remux.' in term and any(i in term for i in AVC):
        return '1080p'
    elif 'remux.' in term:
        return '4k'
    else:
        return 'sd'


def is_anime(content, type, type_id):
    try:
        r = trakt.getGenre(content, type, type_id)
        return 'anime' in r or 'animation' in r
    except:
        return False


def get_release_quality(release_name, release_link=''):

    if not release_name and not release_link: return 'sd', []

    try:
        if release_link:
            term = '.'.join((release_name, cleantitle.get_title(release_link)))
        else:
            term = release_name

        quality = get_qual(term)
        if not quality:
            quality = 'sd'

        info = []
        #if '3d' in fmt or '.3D.' in term: info.append('3D')
        #if any(i in ['hevc', 'h265', 'h.265', 'x265'] for i in term): info.append('HEVC')

        return quality, info
    except:
        return 'sd', []


def getFileType(url):

    try:
        url = cleantitle.get_title(url)
    except:
        url = six.ensure_str(url, errors='ignore')
    url = '.{}.'.format(url).lower()
    type = ''

    if any(i in url for i in ['.bluray.', '.blu.ray.']):
        type += ' BLURAY /'
    if any(i in url for i in ['.bd.r.', '.bdr.', '.bd.rip.', '.bdrip.', '.br.rip.', '.brrip.']):
        type += ' BD-RIP /'
    if 'remux.' in url:
        type += ' REMUX /'
    if any(i in url for i in ['.dvdrip.', '.dvd.rip.']):
        type += ' DVD-RIP /'
    if any(i in url for i in ['.dvd.', '.dvdr.', '.dvd5.', '.dvd9.']):
        type += ' DVD /'
    if any(i in url for i in ['.web.', '.webdl.', '.webrip.']):
        type += ' WEB /'
    if '.hdtv.' in url:
        type += ' HDTV /'
    if '.sdtv.' in url:
        type += ' SDTV /'
    if any(i in url for i in ['.hdrip.', '.hd.rip.']):
        type += ' HDRIP /'
    if any(i in url for i in ['.uhdrip.', '.uhd.rip.']):
        type += ' UHDRIP /'
    if '.r5.' in url:
        type += ' R5 /'
    if any(i in url for i in ['.cam.', '.hdcam.', '.camrip.']):
        type += ' CAM /'
    if any(i in url for i in ['.ts.', '.telesync.', '.hdts.', '.pdvd.']):
        type += ' TS /'
    if any(i in url for i in ['.tc.', '.telecine.', '.hdtc.']):
        type += ' TC /'
    if any(i in url for i in ['.scr.', '.screener.', '.dvdscr.', '.dvd.scr.']):
        type += ' SCR /'
    if '.xvid.' in url:
        type += ' XVID /'
    if '.avi.' in url:
        type += ' AVI /'
    if any(i in url for i in AVC):
        type += ' H.264 /'
    if any(i in url for i in ['.h.265.', '.h256.', '.x265.', '.hevc.']):
        type += ' HEVC /'
    if '.hi10p.' in url:
        type += ' HI10P /'
    if '.10bit.' in url:
        type += ' 10BIT /'
    if '.3d.' in url:
        type += ' 3D /'
    if any(i in url for i in ['.hdr.', '.hdr10.', '.hdr10plus.', '.hlg.']):
        type += ' HDR /'
    if any(i in url for i in ['.dv.', '.dolby.vision.', '.dolbyvision.', '.dovi.']):
        type += ' HDR - DOLBY VISION /'
    if '.imax.' in url:
        type += ' IMAX /'
    if any(i in url for i in ['.ac3.', '.ac.3.']):
        type += ' AC3 /'
    if '.aac.' in url:
        type += ' AAC /'
    if '.aac5.1.' in url:
        type += ' AAC / 5.1 /'
    if any(i in url for i in ['.dd.', '.dolbydigital.', '.dolby.digital.']):
        type += ' DD /'
    if any(i in url for i in ['.truehd.', '.true.hd.']):
        type += ' TRUEHD /'
    if '.atmos.' in url:
        type += ' ATMOS /'
    if any(i in url for i in ['.dolby.digital.plus.', '.dolbydigital.plus.', '.dolbydigitalplus.', '.ddplus.', '.dd.plus.', '.ddp.', '.eac3.', '.eac.3.']):
        type += ' DD+ /'
    if '.dts.' in url:
        type += ' DTS /'
    if any(i in url for i in ['.hdma.', '.hd.ma.']):
        type += ' HD.MA /'
    if any(i in url for i in ['.hdhra.', '.hd.hra.']):
        type += ' HD.HRA /'
    if any(i in url for i in ['.dtsx.', '.dts.x.']):
        type += ' DTS:X /'
    if '.dd5.1.' in url:
        type += ' DD / 5.1 /'
    if '.ddp5.1.' in url:
        type += ' DD+ / 5.1 /'
    if any(i in url for i in ['.5.1.', '.6ch.']):
        type += ' 5.1 /'
    if any(i in url for i in ['.7.1.', '.8ch.']):
        type += ' 7.1 /'
    if '.korsub.' in url:
        type += ' HC-SUBS /'
    if any(i in url for i in ['.subs.', '.subbed.', '.sub.']):
        type += ' SUBS /'
    if any(i in url for i in ['.dub.', '.dubbed.', '.dublado.']):
        type += ' DUB /'
    if '.repack.' in url:
        type += ' REPACK /'
    if '.proper.' in url:
        type += ' PROPER /'
    if '.nuked.' in url:
        type += ' NUKED /'
    type = type.rstrip('/')
    return type


def check_sd_url(release_link):
    try:
        release_link = re.sub('[^A-Za-z0-9]+', '.', release_link)
        release_link = release_link.lower()
        try: release_link = six.ensure_str(release_link)
        except: pass
        quality = get_qual(release_link)
        if not quality:
            quality = 'sd'
        return quality
    except:
        return 'sd'


def check_direct_url(url):
    try:
        url = re.sub('[^A-Za-z0-9]+', '.', url)
        url = six.ensure_str(url)
        url = url.lower()
        quality = get_qual(url)
        if not quality:
            quality = 'sd'
        return quality
    except:
        return 'sd'


def check_url(url):
    try:
        url = client.replaceHTMLCodes(url)
        url = urllib_parse.unquote(url)
        url = re.sub('[^A-Za-z0-9]+', '.', url)
        url = six.ensure_str(url)
        url = url.lower()
    except:
        url = str(url)

    try:
        quality = get_qual(url)
        if not quality:
            quality = 'sd'
        return quality
    except:
        return 'sd'


def label_to_quality(label):
    try:
        try: label = int(re.search('(\d+)', label).group(1))
        except: label = 0

        if label >= 2160:
            return '4K'
        elif label >= 1080:
            return '1080p'
        elif 720 <= label < 1080:
            return '720p'
        elif label < 720:
            return 'sd'
    except:
        return 'sd'


def strip_domain(url):
    try:
        url = six.ensure_str(url)
        if url.lower().startswith('http') or url.startswith('/'):
            url = re.findall('(?://.+?|)(/.+)', url)[0]
        url = client.replaceHTMLCodes(url)
        return url
    except:
        return


def is_host_valid(url, domains):
    try:
        url = six.ensure_str(url).lower()
        if any(x in url for x in ['.rar.', '.zip.', '.iso.']) or any(url.endswith(x) for x in ['.rar', '.zip', '.idx', '.sub', '.srt']):
            return False, ''
        if any(x in url for x in ['sample', 'trailer', 'zippyshare', 'facebook', 'youtu']):
            return False, ''
        host = __top_domain(url)
        hosts = [domain.lower() for domain in domains if host and host in domain.lower()]

        if hosts and '.' not in host:
            host = hosts[0]
        if hosts and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
            host = 'gvideo'
        if hosts and any([h for h in ['akamaized','ocloud'] if h in host]):
            host = 'CDN'
        return any(hosts), host
    except:
        return False, ''


def __top_domain(url):
    if not (url.startswith('//') or url.startswith('http://') or url.startswith('https://')):
        url = '//' + url
    elements = urllib_parse.urlparse(url)
    domain = elements.netloc or elements.path
    domain = domain.split('@')[-1].split(':')[0]
    regex = "(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$"
    res = re.search(regex, domain)
    if res: domain = res.group(1)
    domain = domain.lower()
    return domain


def aliases_to_array(aliases, filter=None):
    try:
        if not filter:
            filter = []
        if isinstance(filter, six.string_types):
            filter = [filter]

        return [x.get('title') for x in aliases if not filter or x.get('country') in filter]
    except:
        return []


def is_match(name, title, hdlr=None, aliases=None):
    try:
        name = name.lower()
        t = re.sub(r'(\+|\.|\(|\[|\s)(\d{4}|s\d+e\d+|s\d+|3d)(\.|\)|\]|\s|)(.+|)', '', name)
        t = cleantitle.get(t)
        titles = [cleantitle.get(title)]

        if aliases:
            if not isinstance(aliases, list):
                from ast import literal_eval
                aliases = literal_eval(aliases)
            try: titles.extend([cleantitle.get(i['title']) for i in aliases])
            except: pass

        if hdlr:
            return (t in titles and hdlr.lower() in name)
        return t in titles
    except:
        log_utils.log('is_match exc', 1)
        return True


def is_season_match(name, title, season, aliases=None):
    name = re.sub('[^\w\s]+', ' ', name)
    name = re.sub(' {2,}', ' ', name).strip().lower()
    t = re.sub(r'(\+|\.|\(|\[|\s)(\d{4}|s\d+e\d+|s\d+|season\s*\d+|complete\s+s|the\s+complete\s+s)(\.|\)|\]|\s|)(.+|)', '', name)
    t = cleantitle.get(t)
    titles = [cleantitle.get(title)]

    if aliases:
        if not isinstance(aliases, list):
            from ast import literal_eval
            aliases = literal_eval(aliases)
        try: titles.extend([cleantitle.get(i['title']) for i in aliases])
        except: pass

    if t in titles:
        season_match = False

        name += ' '
        check = []
        check.append(r'season\s*%s\s+' % season)
        check.append(r'season\s*%s\s+' % season.zfill(2))
        check.append(r's%s\s+' % season)
        check.append(r's%s\s+' % season.zfill(2))
        check.append(r'complete\s+series')
        if any(re.search(c, name) for c in check):
            season_match = True

        else:
            range_match = re.findall(r'(?:s|season)\s*(\d{1,2})\s+(?:to|thru)*\s*(?:s|season)*\s*(\d{1,2})(?:\s|$)', name)
            if range_match:
                if int(range_match[0][0]) <= int(season) <= int(range_match[0][1]):
                    season_match = True

        if not season_match:
            try:
                test_range = re.split(r'(season )|[a-z]', name)
                seasons = test_range[test_range.index('season ') + 1].split()
                if season in seasons or season.zfill(2) in seasons:
                    season_match = True
            except:
                pass

        if season_match:
            no_match = re.search(r'(?:e|ep|episode|episodes)\s*\d{1,2}\s+', name)
            if no_match:
                return False
            return True

    return False


def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib_parse.quote_plus(headers[key])) for key in headers])


def _size(siz):
    if siz in ['0', 0, '', None]: return 0.0, ''
    div = 1 if siz.lower().endswith(('gb', 'gib')) else 1024
    float_size = float(re.sub('[^0-9|/.|/,]', '', siz.replace(',', '.'))) / div
    float_size = round(float_size, 2)
    str_size = '%.2f GB' % float_size
    return float_size, str_size


def get_size(url):
    try:
        size = client.request(url, output='file_size')
        if size == '0': size = False
        size = convert_size(size)
        return size
    except: return False


def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    if size_name[i] == 'B' or size_name[i] == 'KB': return None
    return "%s %s" % (s, size_name[i])


def check_directstreams(url, hoster='', quality='SD'):
    urls = []
    host = hoster

    if 'google' in url or any(x in url for x in ['youtube.', 'docid=']):
        urls = directstream.google(url)
        if not urls:
            tag = directstream.googletag(url)
            if tag: urls = [{'quality': tag[0]['quality'], 'url': url}]
        if urls: host = 'gvideo'
    elif 'ok.ru' in url:
        urls = directstream.odnoklassniki(url)
        if urls: host = 'vk'
    elif 'vk.com' in url:
        urls = directstream.vk(url)
        if urls: host = 'vk'
    elif any(x in url for x in ['akamaized', 'blogspot', 'ocloud.stream']):
        urls = [{'url': url}]
        if urls: host = 'CDN'
        
    direct = True if urls else False

    if not urls: urls = [{'quality': quality, 'url': url}]

    return urls, host, direct


# if salt is provided, it should be string
# ciphertext is base64 and passphrase is string
def evp_decode(cipher_text, passphrase, salt=None):
    cipher_text = six.ensure_text(base64.b64decode(cipher_text))
    if not salt:
        salt = cipher_text[8:16]
        cipher_text = cipher_text[16:]
    data = evpKDF(passphrase, salt)
    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(data['key'], data['iv']))
    plain_text = decrypter.feed(cipher_text)
    plain_text += decrypter.feed()
    return plain_text


def evpKDF(passwd, salt, key_size=8, iv_size=4, iterations=1, hash_algorithm="md5"):
    target_key_size = key_size + iv_size
    derived_bytes = ""
    number_of_derived_words = 0
    block = None
    hasher = hashlib.new(hash_algorithm)
    while number_of_derived_words < target_key_size:
        if block is not None:
            hasher.update(block)

        hasher.update(passwd)
        hasher.update(salt)
        block = hasher.digest()
        hasher = hashlib.new(hash_algorithm)

        for _i in range(1, iterations):
            hasher.update(block)
            block = hasher.digest()
            hasher = hashlib.new(hash_algorithm)

        derived_bytes += block[0: min(len(block), (target_key_size - number_of_derived_words) * 4)]

        number_of_derived_words += len(block) / 4

    return {
        "key": derived_bytes[0: key_size * 4],
        "iv": derived_bytes[key_size * 4:]
    }
