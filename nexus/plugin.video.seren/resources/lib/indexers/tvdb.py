import contextlib
import time
import traceback
from functools import cached_property
from functools import wraps
from math import pi
from math import sin
from urllib import parse

import xbmcgui

from . import valid_id_or_none
from resources.lib.common import tools
from resources.lib.common.thread_pool import ThreadPool
from resources.lib.database.cache import use_cache
from resources.lib.indexers.apibase import ApiBase
from resources.lib.indexers.apibase import handle_single_item_or_list
from resources.lib.modules.exceptions import RanOnceAlready
from resources.lib.modules.global_lock import GlobalLock
from resources.lib.modules.globals import g


def tvdb_guard_response(func):
    @wraps(func)
    def wrapper(*args, **kwarg):
        method_class = args[0]
        import requests

        try:
            response = func(*args, **kwarg)
            if response.status_code in [200, 201]:
                return response

            if response.status_code == 401:
                with contextlib.suppress(RanOnceAlready):
                    with GlobalLock("tvdb.oauth", run_once=True, check_sum=method_class.jwToken) as lock:
                        if method_class.jwToken is not None:
                            method_class.try_refresh_token(True)
                if method_class.refresh_token is not None:
                    return func(*args, **kwarg)

            error_message = (
                TVDBAPI.http_codes[response.status_code] if response.status_code != 404 else response.json()['Error']
            )

            g.log(
                f"TVDB returned a {response.status_code} ({error_message}): while requesting {response.url}",
                "warning" if response.status_code != 404 else "debug",
            )

            return None
        except requests.exceptions.ConnectionError:
            return None
        except Exception:
            xbmcgui.Dialog().notification(g.ADDON_NAME, g.get_language_string(30024).format("TVDB"))
            if g.get_runtime_setting("run.mode") == "test":
                raise
            else:
                g.log_stacktrace()
            return None

    return wrapper


def wrap_tvdb_object(func):
    @wraps(func)
    def wrapper(*args, **kwarg):
        return {"tvdb_object": tvdb_art_sorter(func(*args, **kwarg))}

    return wrapper


def tvdb_art_sorter(item):
    if not item or not item.get("art"):
        return item

    for art_type in ["banner", "poster", "fanart"]:
        if art_type not in item.get("art"):
            continue

        item["art"][art_type] = sorted(
            item["art"][art_type], key=lambda k: (k["language"], k["rating"], k["url"]), reverse=True
        )
    return item


class TVDBAPI(ApiBase):
    baseUrl = "https://api.thetvdb.com/"
    normalization = [
        ("imdbId", ("imdbnumber", "imdb_id"), lambda i: valid_id_or_none(i)),
        ("id", "tvdb_id", None),
        (
            None,
            "rating.tvdb",
            (
                ("siteRating", "siteRatingCount"),
                lambda r, c: {"rating": tools.safe_round(r, 2), "votes": c},
            ),
        ),
        ("firstAired", ("premiered", "aired"), lambda t: g.validate_date(t)),
        ("overview", ("plot", "plotoutline"), None),
        ("mediatype", "mediatype", None),
    ]

    show_normalization = tools.extend_array(
        [
            (
                "firstAired",
                "year",
                lambda t: g.validate_date(t)[:4] if g.validate_date(t) else None,
            ),
            ("status", "status", None),
            ("runtime", "runtime", lambda d: int(d) * 60 if d.isdigit() else None),
            ("network", "studio", None),
            ("genre", "genre", lambda t: sorted(set(t))),
            ("seriesName", ("title", "tvshowtitle"), None),
            ("rating", "mpaa", None),
            ("language", "language", None),
            ("aliases", "aliases", None),
            (
                "country",
                "country_origin",
                lambda t: t.upper() if t is not None else None,
            ),
        ],
        normalization,
    )

    episode_normalization = tools.extend_array(
        [
            ("episodeName", "title", None),
            ("seriesId", "tvdb_show_id", None),
            ("airedEpisodeNumber", ("episode", "sortepisode"), None),
            ("airedSeason", ("season", "sortseason"), None),
            ("directors", "director", lambda t: sorted(set(t))),
            ("writers", "writer", lambda t: sorted(set(t))),
            ("overview", "plot", None),
            ("contentRating", "mpaa", None),
        ],
        normalization,
    )

    meta_objects = {
        "movie": normalization,
        "tvshow": show_normalization,
        "episode": episode_normalization,
    }

    # These are a duplicate of the TMDB codes, should be used as a very rough reference
    # Until we can find a good source from TVDB about their codes we can use this in place
    http_codes = {
        200: "Success",
        201: "Success - new resource created (POST)",
        401: "Returned if your JWT token is missing or expired",
        404: "Returned if the given ID does not exist.",
        409: "Returned if requested record could not be updated/deleted",
        405: "Missing query params are given",
        422: "Invalid query params provided",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
    }

    imageBaseUrl = "https://www.thetvdb.com/banners/"

    art_map = {
        "fanart": "fanart",
        "poster": "poster",
        "season": "poster",
        "seasonwide": "banner",
        "series": "banner",
    }

    supported_languages = [
        {"id": 101, "abbreviation": "aa", "name": "Afaraf", "englishName": "Afar"},
        {
            "id": 102,
            "abbreviation": "ab",
            "name": "?????????? ????????????",
            "englishName": "Abkhaz",
        },
        {
            "id": 103,
            "abbreviation": "af",
            "name": "Afrikaans",
            "englishName": "Afrikaans",
        },
        {"id": 104, "abbreviation": "ak", "name": "Akan", "englishName": "Akan"},
        {"id": 105, "abbreviation": "am", "name": "????????????", "englishName": "Amharic"},
        {
            "id": 106,
            "abbreviation": "ar",
            "name": "??????????????",
            "englishName": "Arabic",
        },
        {
            "id": 107,
            "abbreviation": "an",
            "name": "aragon??s",
            "englishName": "Aragonese",
        },
        {
            "id": 108,
            "abbreviation": "as",
            "name": "?????????????????????",
            "englishName": "Assamese",
        },
        {
            "id": 109,
            "abbreviation": "av",
            "name": "???????? ????????",
            "englishName": "Avaric",
        },
        {
            "id": 110,
            "abbreviation": "ae",
            "name": "avesta",
            "englishName": "Avestan",
        },
        {
            "id": 111,
            "abbreviation": "ay",
            "name": "aymar aru",
            "englishName": "Aymara",
        },
        {
            "id": 112,
            "abbreviation": "az",
            "name": "az??rbaycan dili",
            "englishName": "Azerbaijani",
        },
        {
            "id": 113,
            "abbreviation": "ba",
            "name": "?????????????? ????????",
            "englishName": "Bashkir",
        },
        {
            "id": 114,
            "abbreviation": "bm",
            "name": "bamanankan",
            "englishName": "Bambara",
        },
        {
            "id": 115,
            "abbreviation": "be",
            "name": "???????????????????? ????????",
            "englishName": "Belarusian",
        },
        {
            "id": 116,
            "abbreviation": "bn",
            "name": "???????????????",
            "englishName": "Bengali",
        },
        {
            "id": 117,
            "abbreviation": "bh",
            "name": "?????????????????????",
            "englishName": "Bihari",
        },
        {
            "id": 118,
            "abbreviation": "bi",
            "name": "Bislama",
            "englishName": "Bislama",
        },
        {
            "id": 119,
            "abbreviation": "bo",
            "name": "?????????????????????",
            "englishName": "Tibetan Standard",
        },
        {
            "id": 120,
            "abbreviation": "bs",
            "name": "bosanski jezik",
            "englishName": "Bosnian",
        },
        {
            "id": 121,
            "abbreviation": "br",
            "name": "brezhoneg",
            "englishName": "Breton",
        },
        {
            "id": 122,
            "abbreviation": "bg",
            "name": "?????????????????? ????????",
            "englishName": "Bulgarian",
        },
        {
            "id": 123,
            "abbreviation": "ca",
            "name": "catal??",
            "englishName": "Catalan",
        },
        {"id": 28, "abbreviation": "cs", "name": "??e??tina", "englishName": "Czech"},
        {
            "id": 124,
            "abbreviation": "ch",
            "name": "Chamoru",
            "englishName": "Chamorro",
        },
        {
            "id": 125,
            "abbreviation": "ce",
            "name": "?????????????? ????????",
            "englishName": "Chechen",
        },
        {
            "id": 126,
            "abbreviation": "cu",
            "name": "?????????? ????????????????????",
            "englishName": "Old Church Slavonic",
        },
        {
            "id": 127,
            "abbreviation": "cv",
            "name": "?????????? ??????????",
            "englishName": "Chuvash",
        },
        {
            "id": 128,
            "abbreviation": "kw",
            "name": "Kernewek",
            "englishName": "Cornish",
        },
        {
            "id": 129,
            "abbreviation": "co",
            "name": "corsu",
            "englishName": "Corsican",
        },
        {"id": 130, "abbreviation": "cr", "name": "?????????????????????", "englishName": "Cree"},
        {
            "id": 131,
            "abbreviation": "cy",
            "name": "Cymraeg",
            "englishName": "Welsh",
        },
        {"id": 10, "abbreviation": "da", "name": "dansk", "englishName": "Danish"},
        {
            "id": 14,
            "abbreviation": "de",
            "name": "Deutsch",
            "englishName": "German",
        },
        {
            "id": 132,
            "abbreviation": "dv",
            "name": "????????????",
            "englishName": "Divehi",
        },
        {
            "id": 133,
            "abbreviation": "dz",
            "name": "??????????????????",
            "englishName": "Dzongkha",
        },
        {
            "id": 20,
            "abbreviation": "el",
            "name": "???????????????? ????????????",
            "englishName": "Greek",
        },
        {
            "id": 7,
            "abbreviation": "en",
            "name": "English",
            "englishName": "English",
        },
        {
            "id": 134,
            "abbreviation": "eo",
            "name": "Esperanto",
            "englishName": "Esperanto",
        },
        {
            "id": 135,
            "abbreviation": "et",
            "name": "eesti",
            "englishName": "Estonian",
        },
        {
            "id": 136,
            "abbreviation": "eu",
            "name": "euskara",
            "englishName": "Basque",
        },
        {"id": 137, "abbreviation": "ee", "name": "E??egbe", "englishName": "Ewe"},
        {
            "id": 138,
            "abbreviation": "fo",
            "name": "f??royskt",
            "englishName": "Faroese",
        },
        {
            "id": 139,
            "abbreviation": "fa",
            "name": "??????????",
            "englishName": "Persian",
        },
        {
            "id": 140,
            "abbreviation": "fj",
            "name": "vosa Vakaviti",
            "englishName": "Fijian",
        },
        {"id": 11, "abbreviation": "fi", "name": "suomi", "englishName": "Finnish"},
        {
            "id": 17,
            "abbreviation": "fr",
            "name": "fran??ais",
            "englishName": "French",
        },
        {
            "id": 141,
            "abbreviation": "fy",
            "name": "Frysk",
            "englishName": "Western Frisian",
        },
        {
            "id": 142,
            "abbreviation": "ff",
            "name": "Fulfulde",
            "englishName": "Fula",
        },
        {
            "id": 143,
            "abbreviation": "gd",
            "name": "G??idhlig",
            "englishName": "Scottish Gaelic",
        },
        {
            "id": 144,
            "abbreviation": "ga",
            "name": "Gaeilge",
            "englishName": "Irish",
        },
        {
            "id": 145,
            "abbreviation": "gl",
            "name": "galego",
            "englishName": "Galician",
        },
        {"id": 146, "abbreviation": "gv", "name": "Gaelg", "englishName": "Manx"},
        {
            "id": 147,
            "abbreviation": "gn",
            "name": "Ava??e'???",
            "englishName": "Guaran??",
        },
        {
            "id": 148,
            "abbreviation": "gu",
            "name": "?????????????????????",
            "englishName": "Gujarati",
        },
        {
            "id": 149,
            "abbreviation": "ht",
            "name": "Krey??l ayisyen",
            "englishName": "Haitian",
        },
        {"id": 150, "abbreviation": "ha", "name": "????????????", "englishName": "Hausa"},
        {"id": 24, "abbreviation": "he", "name": "??????????", "englishName": "Hebrew"},
        {
            "id": 151,
            "abbreviation": "hz",
            "name": "Otjiherero",
            "englishName": "Herero",
        },
        {"id": 152, "abbreviation": "hi", "name": "??????????????????", "englishName": "Hindi"},
        {
            "id": 153,
            "abbreviation": "ho",
            "name": "Hiri Motu",
            "englishName": "Hiri Motu",
        },
        {
            "id": 31,
            "abbreviation": "hr",
            "name": "hrvatski jezik",
            "englishName": "Croatian",
        },
        {
            "id": 19,
            "abbreviation": "hu",
            "name": "Magyar",
            "englishName": "Hungarian",
        },
        {
            "id": 154,
            "abbreviation": "hy",
            "name": "??????????????",
            "englishName": "Armenian",
        },
        {
            "id": 155,
            "abbreviation": "ig",
            "name": "As???s??? Igbo",
            "englishName": "Igbo",
        },
        {"id": 156, "abbreviation": "io", "name": "Ido", "englishName": "Ido"},
        {
            "id": 157,
            "abbreviation": "ii",
            "name": "Nuosuhxop",
            "englishName": "Nuosu",
        },
        {
            "id": 158,
            "abbreviation": "iu",
            "name": "??????????????????",
            "englishName": "Inuktitut",
        },
        {
            "id": 159,
            "abbreviation": "ie",
            "name": "Interlingue",
            "englishName": "Interlingue",
        },
        {
            "id": 160,
            "abbreviation": "ia",
            "name": "Interlingua",
            "englishName": "Interlingua",
        },
        {
            "id": 161,
            "abbreviation": "id",
            "name": "Bahasa Indonesia",
            "englishName": "Indonesian",
        },
        {
            "id": 162,
            "abbreviation": "ik",
            "name": "I??upiaq",
            "englishName": "Inupiaq",
        },
        {
            "id": 163,
            "abbreviation": "is",
            "name": "??slenska",
            "englishName": "Icelandic",
        },
        {
            "id": 15,
            "abbreviation": "it",
            "name": "italiano",
            "englishName": "Italian",
        },
        {
            "id": 164,
            "abbreviation": "jv",
            "name": "basa Jawa",
            "englishName": "Javanese",
        },
        {"id": 25, "abbreviation": "ja", "name": "?????????", "englishName": "Japanese"},
        {
            "id": 165,
            "abbreviation": "kl",
            "name": "kalaallisut",
            "englishName": "Kalaallisut",
        },
        {
            "id": 166,
            "abbreviation": "kn",
            "name": "???????????????",
            "englishName": "Kannada",
        },
        {
            "id": 167,
            "abbreviation": "ks",
            "name": "?????????????????????",
            "englishName": "Kashmiri",
        },
        {
            "id": 168,
            "abbreviation": "ka",
            "name": "?????????????????????",
            "englishName": "Georgian",
        },
        {
            "id": 169,
            "abbreviation": "kr",
            "name": "Kanuri",
            "englishName": "Kanuri",
        },
        {
            "id": 170,
            "abbreviation": "kk",
            "name": "?????????? ????????",
            "englishName": "Kazakh",
        },
        {"id": 171, "abbreviation": "km", "name": "???????????????", "englishName": "Khmer"},
        {
            "id": 172,
            "abbreviation": "ki",
            "name": "G??k??y??",
            "englishName": "Kikuyu",
        },
        {
            "id": 173,
            "abbreviation": "rw",
            "name": "Ikinyarwanda",
            "englishName": "Kinyarwanda",
        },
        {
            "id": 174,
            "abbreviation": "ky",
            "name": "???????????? ????????",
            "englishName": "Kirghiz",
        },
        {
            "id": 175,
            "abbreviation": "kv",
            "name": "???????? ??????",
            "englishName": "Komi",
        },
        {
            "id": 176,
            "abbreviation": "kg",
            "name": "KiKongo",
            "englishName": "Kongo",
        },
        {"id": 32, "abbreviation": "ko", "name": "?????????", "englishName": "Korean"},
        {
            "id": 177,
            "abbreviation": "kj",
            "name": "Kuanyama",
            "englishName": "Kwanyama",
        },
        {
            "id": 178,
            "abbreviation": "ku",
            "name": "Kurd??",
            "englishName": "Kurdish",
        },
        {"id": 179, "abbreviation": "lo", "name": "?????????????????????", "englishName": "Lao"},
        {"id": 180, "abbreviation": "la", "name": "latine", "englishName": "Latin"},
        {
            "id": 181,
            "abbreviation": "lv",
            "name": "latvie??u valoda",
            "englishName": "Latvian",
        },
        {
            "id": 182,
            "abbreviation": "li",
            "name": "Limburgs",
            "englishName": "Limburgish",
        },
        {
            "id": 183,
            "abbreviation": "ln",
            "name": "Ling??la",
            "englishName": "Lingala",
        },
        {
            "id": 184,
            "abbreviation": "lt",
            "name": "lietuvi?? kalba",
            "englishName": "Lithuanian",
        },
        {
            "id": 185,
            "abbreviation": "lb",
            "name": "L??tzebuergesch",
            "englishName": "Luxembourgish",
        },
        {
            "id": 186,
            "abbreviation": "lu",
            "name": "Luba-Katanga",
            "englishName": "Luba-Katanga",
        },
        {
            "id": 187,
            "abbreviation": "lg",
            "name": "Luganda",
            "englishName": "Luganda",
        },
        {
            "id": 188,
            "abbreviation": "mh",
            "name": "Kajin M??aje??",
            "englishName": "Marshallese",
        },
        {
            "id": 189,
            "abbreviation": "ml",
            "name": "??????????????????",
            "englishName": "Malayalam",
        },
        {
            "id": 190,
            "abbreviation": "mr",
            "name": "???????????????",
            "englishName": "Marathi",
        },
        {
            "id": 191,
            "abbreviation": "mk",
            "name": "???????????????????? ??????????",
            "englishName": "Macedonian",
        },
        {
            "id": 192,
            "abbreviation": "mg",
            "name": "Malagasy fiteny",
            "englishName": "Malagasy",
        },
        {
            "id": 193,
            "abbreviation": "mt",
            "name": "Malti",
            "englishName": "Maltese",
        },
        {
            "id": 194,
            "abbreviation": "mn",
            "name": "????????????",
            "englishName": "Mongolian",
        },
        {
            "id": 195,
            "abbreviation": "mi",
            "name": "te reo M??ori",
            "englishName": "M??ori",
        },
        {
            "id": 196,
            "abbreviation": "ms",
            "name": "bahasa Melayu",
            "englishName": "Malay",
        },
        {
            "id": 197,
            "abbreviation": "my",
            "name": "Burmese",
            "englishName": "Burmese",
        },
        {
            "id": 198,
            "abbreviation": "na",
            "name": "Ekakair?? Naoero",
            "englishName": "Nauru",
        },
        {
            "id": 199,
            "abbreviation": "nv",
            "name": "Din?? bizaad",
            "englishName": "Navajo",
        },
        {
            "id": 200,
            "abbreviation": "nr",
            "name": "isiNdebele",
            "englishName": "South Ndebele",
        },
        {
            "id": 201,
            "abbreviation": "nd",
            "name": "isiNdebele",
            "englishName": "North Ndebele",
        },
        {
            "id": 202,
            "abbreviation": "ng",
            "name": "Owambo",
            "englishName": "Ndonga",
        },
        {
            "id": 203,
            "abbreviation": "ne",
            "name": "??????????????????",
            "englishName": "Nepali",
        },
        {
            "id": 13,
            "abbreviation": "nl",
            "name": "Nederlands",
            "englishName": "Dutch",
        },
        {
            "id": 9,
            "abbreviation": "no",
            "name": "Norsk bokm??l",
            "englishName": "Norwegian",
        },
        {
            "id": 206,
            "abbreviation": "ny",
            "name": "chiChe??a",
            "englishName": "Chichewa",
        },
        {
            "id": 207,
            "abbreviation": "oc",
            "name": "occitan",
            "englishName": "Occitan",
        },
        {
            "id": 208,
            "abbreviation": "oj",
            "name": "????????????????????????",
            "englishName": "Ojibwe",
        },
        {"id": 209, "abbreviation": "or", "name": "???????????????", "englishName": "Oriya"},
        {
            "id": 210,
            "abbreviation": "om",
            "name": "Afaan Oromoo",
            "englishName": "Oromo",
        },
        {
            "id": 211,
            "abbreviation": "os",
            "name": "???????? ??????????",
            "englishName": "Ossetian",
        },
        {
            "id": 212,
            "abbreviation": "pa",
            "name": "??????????????????",
            "englishName": "Panjabi",
        },
        {"id": 213, "abbreviation": "pi", "name": "????????????", "englishName": "P??li"},
        {
            "id": 18,
            "abbreviation": "pl",
            "name": "j??zyk polski",
            "englishName": "Polish",
        },
        {
            "id": 214,
            "abbreviation": "pt",
            "name": "Portugu??s - Portugal",
            "englishName": "Portuguese - Portugal",
        },
        {
            "id": 26,
            "abbreviation": "pt",
            "name": "Portugu??s - Brasil",
            "englishName": "Portuguese - Brazil",
        },
        {"id": 215, "abbreviation": "ps", "name": "????????", "englishName": "Pashto"},
        {
            "id": 216,
            "abbreviation": "qu",
            "name": "Runa Simi",
            "englishName": "Quechua",
        },
        {
            "id": 217,
            "abbreviation": "rm",
            "name": "rumantsch grischun",
            "englishName": "Romansh",
        },
        {
            "id": 218,
            "abbreviation": "ro",
            "name": "limba rom??n??",
            "englishName": "Romanian",
        },
        {
            "id": 219,
            "abbreviation": "rn",
            "name": "Ikirundi",
            "englishName": "Kirundi",
        },
        {
            "id": 22,
            "abbreviation": "ru",
            "name": "?????????????? ????????",
            "englishName": "Russian",
        },
        {
            "id": 220,
            "abbreviation": "sg",
            "name": "y??ng?? t?? s??ng??",
            "englishName": "Sango",
        },
        {
            "id": 221,
            "abbreviation": "sa",
            "name": "???????????????????????????",
            "englishName": "Sanskrit",
        },
        {
            "id": 222,
            "abbreviation": "si",
            "name": "???????????????",
            "englishName": "Sinhala",
        },
        {
            "id": 30,
            "abbreviation": "sk",
            "name": "sloven??ina",
            "englishName": "Slovak",
        },
        {
            "id": 223,
            "abbreviation": "sl",
            "name": "slovenski jezik",
            "englishName": "Slovene",
        },
        {
            "id": 224,
            "abbreviation": "se",
            "name": "Davvis??megiella",
            "englishName": "Northern Sami",
        },
        {
            "id": 225,
            "abbreviation": "sm",
            "name": "gagana fa'a Samoa",
            "englishName": "Samoan",
        },
        {
            "id": 226,
            "abbreviation": "sn",
            "name": "chiShona",
            "englishName": "Shona",
        },
        {
            "id": 227,
            "abbreviation": "sd",
            "name": "??????????????????",
            "englishName": "Sindhi",
        },
        {
            "id": 228,
            "abbreviation": "so",
            "name": "Soomaaliga",
            "englishName": "Somali",
        },
        {
            "id": 229,
            "abbreviation": "st",
            "name": "Sesotho",
            "englishName": "Southern Sotho",
        },
        {
            "id": 16,
            "abbreviation": "es",
            "name": "espa??ol",
            "englishName": "Spanish",
        },
        {
            "id": 230,
            "abbreviation": "sq",
            "name": "gjuha shqipe",
            "englishName": "Albanian",
        },
        {
            "id": 231,
            "abbreviation": "sc",
            "name": "sardu",
            "englishName": "Sardinian",
        },
        {
            "id": 232,
            "abbreviation": "sr",
            "name": "???????????? ??????????",
            "englishName": "Serbian",
        },
        {
            "id": 233,
            "abbreviation": "ss",
            "name": "SiSwati",
            "englishName": "Swati",
        },
        {
            "id": 234,
            "abbreviation": "su",
            "name": "Basa Sunda",
            "englishName": "Sundanese",
        },
        {
            "id": 235,
            "abbreviation": "sw",
            "name": "Kiswahili",
            "englishName": "Swahili",
        },
        {
            "id": 8,
            "abbreviation": "sv",
            "name": "svenska",
            "englishName": "Swedish",
        },
        {
            "id": 236,
            "abbreviation": "ty",
            "name": "Reo Tahiti",
            "englishName": "Tahitian",
        },
        {"id": 237, "abbreviation": "ta", "name": "???????????????", "englishName": "Tamil"},
        {
            "id": 238,
            "abbreviation": "tt",
            "name": "?????????? ????????",
            "englishName": "Tatar",
        },
        {
            "id": 239,
            "abbreviation": "te",
            "name": "??????????????????",
            "englishName": "Telugu",
        },
        {"id": 240, "abbreviation": "tg", "name": "????????????", "englishName": "Tajik"},
        {
            "id": 241,
            "abbreviation": "tl",
            "name": "Wikang Tagalog",
            "englishName": "Tagalog",
        },
        {"id": 242, "abbreviation": "th", "name": "?????????", "englishName": "Thai"},
        {
            "id": 243,
            "abbreviation": "ti",
            "name": "????????????",
            "englishName": "Tigrinya",
        },
        {
            "id": 244,
            "abbreviation": "to",
            "name": "faka Tonga",
            "englishName": "Tonga",
        },
        {
            "id": 245,
            "abbreviation": "tn",
            "name": "Setswana",
            "englishName": "Tswana",
        },
        {
            "id": 246,
            "abbreviation": "ts",
            "name": "Xitsonga",
            "englishName": "Tsonga",
        },
        {
            "id": 247,
            "abbreviation": "tk",
            "name": "T??rkmen",
            "englishName": "Turkmen",
        },
        {
            "id": 21,
            "abbreviation": "tr",
            "name": "T??rk??e",
            "englishName": "Turkish",
        },
        {"id": 248, "abbreviation": "tw", "name": "Twi", "englishName": "Twi"},
        {
            "id": 249,
            "abbreviation": "ug",
            "name": "Uy??urq??",
            "englishName": "Uighur",
        },
        {
            "id": 250,
            "abbreviation": "uk",
            "name": "???????????????????? ????????",
            "englishName": "Ukrainian",
        },
        {"id": 251, "abbreviation": "ur", "name": "????????", "englishName": "Urdu"},
        {"id": 252, "abbreviation": "uz", "name": "Ozbek", "englishName": "Uzbek"},
        {
            "id": 253,
            "abbreviation": "ve",
            "name": "Tshiven???a",
            "englishName": "Venda",
        },
        {
            "id": 254,
            "abbreviation": "vi",
            "name": "Ti???ng Vi???t",
            "englishName": "Vietnamese",
        },
        {
            "id": 255,
            "abbreviation": "vo",
            "name": "Volap??k",
            "englishName": "Volap??k",
        },
        {
            "id": 256,
            "abbreviation": "wa",
            "name": "walon",
            "englishName": "Walloon",
        },
        {"id": 257, "abbreviation": "wo", "name": "Wollof", "englishName": "Wolof"},
        {
            "id": 258,
            "abbreviation": "xh",
            "name": "isiXhosa",
            "englishName": "Xhosa",
        },
        {
            "id": 259,
            "abbreviation": "yi",
            "name": "????????????",
            "englishName": "Yiddish",
        },
        {
            "id": 260,
            "abbreviation": "yo",
            "name": "Yor??b??",
            "englishName": "Yoruba",
        },
        {
            "id": 261,
            "abbreviation": "za",
            "name": "Sa?? cue????",
            "englishName": "Zhuang",
        },
        {
            "id": 27,
            "abbreviation": "zh",
            "name": "????????????",
            "englishName": "Chinese - China",
        },
        {"id": 262, "abbreviation": "zu", "name": "isiZulu", "englishName": "Zulu"},
    ]

    def __init__(self):

        self._load_settings()

        self.lang_code = g.get_language_code(False)

        self.languages = (
            [None, self.lang_code]
            if self.lang_code != "en" and any(self.lang_code == i["abbreviation"] for i in self.supported_languages)
            else [None]
        )

        if not self.jwToken:
            self.init_token()
        else:
            self.try_refresh_token()

        self.preferred_artwork_size = g.get_int_setting("artwork.preferredsize")

    @cached_property
    def meta_hash(self):
        return tools.md5_hash(
            (
                self.lang_code,
                self.art_map,
                self.baseUrl,
                self.imageBaseUrl,
                self.preferred_artwork_size,
            )
        )

    @cached_property
    def session(self):
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3 import Retry

        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount("https://", HTTPAdapter(max_retries=retries, pool_maxsize=100))
        return session

    @cached_property
    def threadpool(self):
        return ThreadPool()

    def _get_headers(self, lang=None):
        headers = {"content-type": "application/json"}

        if self.jwToken:
            headers["Authorization"] = f"Bearer {self.jwToken}"
        if lang is not None:
            headers["Accept-Language"] = lang
        return headers

    def try_refresh_token(self, force=False):
        if not force and self.tokenExpires > float(time.time()):
            return
        try:
            with GlobalLock(self.__class__.__name__, True, self.jwToken) as lock:
                try:
                    g.log("TVDB Token requires refreshing...")
                    response = self.session.post(
                        parse.urljoin(self.baseUrl, "refresh_token"),
                        headers=self._get_headers(),
                    ).json()
                    if "Error" in response:
                        response = self.session.post(
                            f"{self.baseUrl}login",
                            json={"apikey": self.apiKey},
                            headers=self._get_headers(),
                        ).json()
                    self._save_settings(response)
                    g.log("Refreshed Tvdbs Token")
                except Exception:
                    g.log("Failed to refresh Tvdb Access Token", "error")
                    return
        except RanOnceAlready:
            return

    def _load_settings(self):
        self.apiKey = g.get_setting("tvdb.apikey", "43VPI0R8323FB7TI")
        self.jwToken = g.get_setting("tvdb.jw")
        self.tokenExpires = g.get_float_setting("tvdb.expiry")

    def _save_settings(self, response):
        if "token" in response:
            g.set_setting("tvdb.jw", response["token"])
            self.jwToken = response["token"]
            self.tokenExpires = time.time() + (24 * (60 * 60))
            g.set_setting("tvdb.expiry", str(self.tokenExpires))

    def init_token(self):
        try:
            with GlobalLock(self.__class__.__name__, True):
                response = self.session.post(
                    f"{self.baseUrl}login",
                    json={"apikey": self.apiKey},
                    headers=self._get_headers(),
                ).json()
                self._save_settings(response)
        except RanOnceAlready:
            return

    @tvdb_guard_response
    def get(self, url, **params):
        language = params.pop("language") if "language" in params else None
        timeout = params.pop("timeout", 10)
        return self.session.get(
            self.baseUrl + url,
            params=params,
            headers=self._get_headers(language),
            timeout=timeout,
        )

    @staticmethod
    def _flatten(response):
        if "data" in response:
            response = response["data"]
        return response or []

    def get_json(self, url, **params):
        response = self.get(url, **params)
        if response is None:
            return None
        try:
            return self._handle_response(params.get("language"), self._flatten(response.json()))
        except (ValueError, AttributeError):
            traceback.print_exc()
            g.log(
                f"Failed to receive JSON from Tvdb response - response: {response}",
                "error",
            )
            return None

    @use_cache()
    def get_json_cached(self, url, **params):
        return self.get_json(url, **params)

    @staticmethod
    def _get_all_pages(func, url, **params):
        progress_callback = params.pop("progress") if "progress" in params else None
        response = func(url, **params)
        yield response
        if "links" not in response.headers:
            return
        for i in range(2, int(response.headers["X-Pagination-Page-Count"]) + 1):
            if callable(progress_callback):
                progress_callback(  # pylint: disable=not-callable
                    (i / (int(response.headers["X-Pagination-Page-Count"]) + 1)) * 100
                )
            params["page"] = i
            yield func(url, **params)

    @handle_single_item_or_list
    def _handle_response(self, language, item):
        item = self._try_detect_type(item)
        if "mediatype" not in item:
            return item

        return {
            "art": self._extract_art(item, language),
            "info": self._normalize_info(self.meta_objects[item["mediatype"]], item),
        }

    @handle_single_item_or_list
    def _handle_cast(self, item):
        if item is None or "name" not in item:
            return {}
        return {
            "name": item["name"],
            "role": item["role"],
            "thumbnail": self._get_absolute_image_path(item["image"]),
            "order": item["sortOrder"],
        }

    @staticmethod
    def _try_detect_type(item):
        if "airedSeasons" in item or "seriesName" in item:
            item.update({"mediatype": "tvshow"})
        elif "episodeName" in item:
            item.update({"mediatype": "episode"})
        return item

    def _extract_art(self, item, language, key_name=None, sub_key=None):
        result = {}
        if item is None:
            return result

        if isinstance(item, dict) and item.get("filename"):
            result["thumb"] = self._get_absolute_image_path(item["filename"])

        if key_name is not None and isinstance(item, list):
            if art := [
                self._get_image(i, self.art_map[key_name], language)
                for i in item
                if "fileName" in i
                and i.get("keyType") == key_name
                and (sub_key is None or i.get("subKey") == str(sub_key))
            ]:
                result[self.art_map[key_name]] = art
        return result

    @staticmethod
    def _get_rating(image):
        if not image["ratingsInfo"]["count"]:
            return 5
        info = image["ratingsInfo"]
        rating = info["average"]
        if info["count"] < 5:
            rating = 5 + (rating - 5) * sin(info["count"] / pi)
        return rating

    @staticmethod
    def _parse_size(image, art_type):
        if art_type in ("series", "seasonwide"):
            return 758
        elif art_type == "season":
            return 1000
        try:
            return int(image["resolution"].split("x")[0 if art_type != "poster" else 1])
        except (ValueError, IndexError):
            return 0

    def _get_image(self, image, art_type, language):
        return {
            "url": self._get_absolute_image_path(image["fileName"]),
            "language": language or "en",
            "rating": self._get_rating(image),
            "size": self._parse_size(image, art_type),
        }

    @wrap_tvdb_object
    def get_show(self, tvdb_id):
        art_types = [i for i in self._get_show_art_types(tvdb_id) or [] if not i.startswith("season")]
        threadpool = ThreadPool()
        threadpool.put(self._get_series_cast, tvdb_id)
        for language in self.languages:
            threadpool.put(self._get_show_info, tvdb_id, language)
            for art_type in art_types:
                threadpool.put(self._get_show_art, tvdb_id, art_type, language)
        item = threadpool.wait_completion()

        return item or None

    @wrap_tvdb_object
    def get_show_art(self, tvdb_id):
        item = self.threadpool.map_results(
            self._get_show_art,
            (
                (tvdb_id, art_type, language)
                for language in self.languages
                for art_type in self._get_show_art_types(tvdb_id) or []
                if not art_type.startswith("season")
            ),
        )

        return item or None

    @wrap_tvdb_object
    def get_show_info(self, tvdb_id):
        threadpool = ThreadPool()
        threadpool.put(self._get_series_cast, tvdb_id)
        for language in self.languages:
            threadpool.put(self._get_show_info, tvdb_id, language)
        item = threadpool.wait_completion()

        return item or None

    @wrap_tvdb_object
    def get_show_rating(self, tvdb_id):
        item = self.get_json_cached(
            f"series/{tvdb_id}/filter",
            keys="siteRating,siteRatingCount,seriesName",
        )

        return {"info": tools.filter_dictionary(item["info"], "rating.tvdb")} if item else None

    @wrap_tvdb_object
    def get_show_cast(self, tvdb_id):
        cast = self._get_series_cast(tvdb_id)
        return cast if cast.get("cast") else None

    @use_cache()
    def _get_show_art_types(self, tvdb_id):
        result = self.get_json_cached(f"series/{tvdb_id}/images/query/params")
        return sorted([i["keyType"] for i in result if "keyType" in i]) if result else result

    def _get_show_art(self, tvdb_id, key_type, language):
        return {
            "art": self._extract_art(
                self.get_json_cached(
                    f"series/{tvdb_id}/images/query?keyType={key_type}",
                    language=language,
                ),
                language,
                key_type,
            )
        }

    def _get_show_info(self, tvdb_id, language):
        return self.get_json_cached(f"series/{tvdb_id}", language=language)

    def _get_series_cast(self, tvdb_id):
        return {"cast": self._handle_cast(self.get_json_cached(f"series/{tvdb_id}/actors"))}

    @wrap_tvdb_object
    def get_season_art(self, tvdb_id, season):
        art_types = self._get_show_art_types(tvdb_id)
        if not art_types:
            return

        item = self.threadpool.map_results(
            self._get_season_art,
            (
                (tvdb_id, art_type, season, language)
                for language in self.languages
                for art_type in art_types
                if art_type.startswith("season")
            ),
        )
        return item or None

    def _get_season_art(self, tvdb_id, art_name, season, language):
        return {
            "art": self._extract_art(
                self.get_json_cached(
                    f"series/{tvdb_id}/images/query",
                    keyType=art_name,
                    language=language,
                ),
                language,
                art_name,
                season,
            )
        }

    def _get_episode_info(self, tvdb_id, season, episode, language):
        if result := self.get_json_cached(
            f"series/{tvdb_id}/episodes/query", airedSeason=season, airedEpisode=episode, language=language
        ):
            return result[0] if isinstance(result, list) else result
        else:
            return None

    @wrap_tvdb_object
    def get_episode(self, tvdb_id, season, episode):
        item = self.threadpool.map_results(
            self._get_episode_info, args_iterable=((tvdb_id, season, episode, language) for language in self.languages)
        )
        return item or None

    @wrap_tvdb_object
    def get_episode_rating(self, tvdb_id, season, episode):
        item = self._get_episode_info(tvdb_id, season, episode, None)

        return {"info": tools.filter_dictionary(item["info"], "rating.tvdb")} if item else None

    def _get_absolute_image_path(self, relative_path):
        if not relative_path:
            return None
        if self.preferred_artwork_size == 2:
            splitted_path = relative_path.split(".")
            relative_path = f"{splitted_path[0]}_t.{splitted_path[1]}"
        return "/".join([self.imageBaseUrl.strip("/"), relative_path.strip("/")])
