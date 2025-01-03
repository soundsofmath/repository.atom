import requests, re

from ..util import m3u8_src

from ..models.Extractor import Extractor
from ..models.Link import Link

class VeCDN(Extractor):
    def __init__(self) -> None:
        self.domains = [".+vecdn.pw", "focus4ca.com"]
        self.domains_regex = True

    def get_link(self, url):
        r = requests.get(url).text
        fid = re.findall(r"fid=[\"'](.+?)[\"']", r)[0]
        r_ragnaru = requests.get(f"https://{self.domains[1]}/embed.php?player=desktop&live=" + fid, headers={"Referer": url}).text
        # m3u8 = "".join(eval(re.findall(r"return\((\[.+?\])", r_ragnaru)[0])).replace("\\", "")

        m3u8 = m3u8_src.scan_page(url, r_ragnaru)
        if m3u8 != None:
            address = m3u8.address
        else:
            address = "".join(eval(re.findall(r'return\((\["h","t".+?\])', r_ragnaru)[0])).replace("\\", "").replace("////", "//")
        return Link(address=address, headers={"Referer": f"https://{self.domains[1]}/"})