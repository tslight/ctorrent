import requests
from urllib.parse import quote
from .utils import get_hr_size

class TPB:
    def __init__(self):
        self.base_url = "https://apibay.org"

    def get_magnet(self, info_hash, torrent_name):
        trackers = (
            "&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3"+
            "A%2F%2F9.rarbg.me%3A2850%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A29"+
            "20%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%"+
            "3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce"
        )
        return f"magnet:?xt=urn:btih:{info_hash}&dn={quote(torrent_name)}{trackers}"

    def search(self, query):
        url = f"{self.base_url}/q.php?q={query}"
        results = requests.get(url).json()
        results = sorted(results, key=lambda d: int(d["size"]), reverse=True)

        for result in results:
            result['magnet'] = self.get_magnet(result['info_hash'], result['name'])
            result['size'] = get_hr_size(result['size'])

        return results

class SolidTorrents:
    def __init__(self):
        self.base_url = "https://solidtorrents.net"

    def search(self, query, sort_by):
        url = f"{self.base_url}/api/v1/search?sort={sort_by}&q={query}"
        results = requests.get(url).json()
        results = sorted(results, key=lambda d: int(d["size"]), reverse=True)
