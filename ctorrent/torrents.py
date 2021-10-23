import math
import requests
from urllib.parse import quote, urlencode
from .utils import get_hr_size, get_key_from_value


def get_magnet(info_hash, torrent_name):
    trackers = [
        "udp://tracker.coppersurfer.tk:6969/announce",
        "udp://9.rarbg.me:2850/announce",
        "udp://9.rarbg.to:2920/announce",
        "udp://tracker.opentrackr.org:1337",
        "udp://tracker.internetwarriors.net:1337/announce",
        "udp://tracker.leechers-paradise.org:6969/announce",
        "udp://tracker.pirateparty.gr:6969/announce",
        "udp://tracker.cyberia.is:6969/announce",
    ]
    trackers = "".join([f"&tr={quote(t, safe='')}" for t in trackers])
    name = quote(torrent_name, safe="")
    return f"magnet:?xt=urn:btih:{info_hash}&dn={name}{trackers}"


class CSV:
    def __init__(self):
        self.base_url = "https://torrents-csv.ml"

    def search(self, query, category, order):
        url = f"{self.base_url}/service/search?size=100&q={query}"
        results = requests.get(url).json()
        if order == "size":
            order = "size_bytes"
        results = sorted(results, key=lambda d: int(d[order]), reverse=True)
        torrents = []

        for result in results:
            torrents.append(
                {
                    "Name": result["name"],
                    "Size": get_hr_size(result["size_bytes"]),
                    "size": result["size_bytes"],
                    "SE": result["seeders"],
                    "LE": result["leechers"],
                    "seeders": result["seeders"],
                    "leechers": result["leechers"],
                    "Category": "N/A",
                    "Site": "Torrents CSV",
                    "Magnet": get_magnet(result["infohash"], result["name"]),
                }
            )

        return torrents


class Solid:
    def __init__(self):
        self.base_url = "https://solidtorrents.net/api/v1"
        self.session = requests.session()
        self.categories = {
            "all": ["all"],
            "audio": ["audio"],
            "video": ["video"],
            "games": ["program", "android"],
            "apps": [
                "program",
                "android",
                "archive",
                "discimage",
                "sourcecode",
                "database",
            ],
            "other": ["image", "document", "ebook", "database"],
        }

    def generate_results(self, query, category, order):
        current, total = 0, 1

        while current < total:
            params = {
                "category": "+".join(self.categories[category]),
                "q": query,
                "sort": order,
                "skip": current,
                "fuv": "yes",
            }
            url = f"{self.base_url}/search?{urlencode(params)}"
            data = self.session.get(url).json()
            total = data["hits"]["value"]
            current += 20
            yield from data["results"]

    def search(self, query, category, order):
        all_pages = []
        for content in self.generate_results(query, category, order):
            all_pages.append(content)

        torrents = []

        for result in all_pages:
            torrents.append(
                {
                    "Name": result["title"],
                    "Size": get_hr_size(result["size"]),
                    "size": result["size"],
                    "SE": result["swarm"]["seeders"],
                    "LE": result["swarm"]["leechers"],
                    "seeders": result["swarm"]["seeders"],
                    "leechers": result["swarm"]["leechers"],
                    "Category": result["category"],
                    "Site": "Solid Torrents",
                    "Magnet": result["magnet"],
                }
            )

        return torrents


class TPB:
    def __init__(self):
        self.base_url = "https://apibay.org"
        self.categories = {
            "all": "",
            "audio": "100",
            "video": "200",
            "apps": "300",
            "games": "400",
            "porn": "500",
            "other": "600",
        }

    def search(self, query, category, order):
        url = f"{self.base_url}/q.php?q={query}&cat={self.categories[category]}"
        results = requests.get(url).json()
        results = sorted(results, key=lambda d: int(d[order]), reverse=True)
        torrents = []

        for result in results:
            cat = int(math.floor(float(result["category"]) / 100.0)) * 100
            torrents.append(
                {
                    "Name": result["name"],
                    "Size": get_hr_size(result["size"]),
                    "size": result["size"],
                    "SE": result["seeders"],
                    "LE": result["leechers"],
                    "seeders": result["seeders"],
                    "leechers": result["leechers"],
                    "Category": get_key_from_value(self.categories, str(cat)),
                    "Site": "The Pirate Bay",
                    "Magnet": get_magnet(result["info_hash"], result["name"]),
                }
            )

        return torrents
