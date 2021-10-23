import math
import requests
from urllib.parse import quote
from .utils import get_hr_size, get_key_from_value


class TPB:
    def __init__(self):
        self.base_url = "https://apibay.org"
        self.categories = {
            "All": "",
            "Audio": "100",
            "Video": "200",
            "Apps": "300",
            "Games": "400",
            "Porn": "500",
            "Other": "600",
        }

    def get_magnet(self, info_hash, torrent_name):
        # trackers_og = (
        #     "&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce"
        #     + "&tr=udp%3A%2F%2F9.rarbg.me%3A2850%2Fannounce"
        #     + "&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce"
        #     + "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337"
        #     + "&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce"
        # )

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

    def search(self, query, category):
        url = f"{self.base_url}/q.php?q={query}&cat={self.categories[category]}"
        results = requests.get(url).json()
        results = sorted(results, key=lambda d: int(d["size"]), reverse=True)
        torrents = []

        for result in results:
            cat = int(math.floor(float(result["category"]) / 100.0)) * 100
            torrents.append(
                {
                    "Name": result["name"],
                    "Size": get_hr_size(result["size"]),
                    "SE": result["leechers"],
                    "LE": result["leechers"],
                    "Site": "The Pirate Bay",
                    "Category": get_key_from_value(self.categories, str(cat)),
                    "Magnet": self.get_magnet(result["info_hash"], result["name"]),
                }
            )

        return torrents


class TorrentsCSV:
    def __init__(self):
        self.base_url = "https://torrents-csv.ml"

    def get_magnet(self, info_hash, torrent_name):
        trackers = (
            "&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3"
            + "A%2F%2F9.rarbg.me%3A2850%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A29"
            + "20%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%"
            + "3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce"
        )
        return f"magnet:?xt=urn:btih:{info_hash}&dn={quote(torrent_name)}{trackers}"

    def search(self, query):
        url = f"{self.base_url}/service/search?size=100&q={query}"
        results = requests.get(url).json()
        results = sorted(results, key=lambda d: int(d["size_bytes"]), reverse=True)
        torrents = []

        for result in results:
            torrents.append(
                {
                    "Name": result["name"],
                    "Size": get_hr_size(result["size_bytes"]),
                    "SE": result["leechers"],
                    "LE": result["leechers"],
                    "Site": "Torrents CSV",
                    "Magnet": self.get_magnet(result["infohash"], result["name"]),
                }
            )

        return torrents


class Solid:
    def __init__(self):
        self.base_url = "https://solidtorrents.net/api/v1"
        self.session = requests.session()

    def generate_results(self, query, sort_by="size", category="all"):
        current, total = 0, 1

        while current < total:
            url = (
                f"{self.base_url}/search?"
                + f"sort={sort_by}&"
                + f"skip={current}&"
                + f"q={query}"
            )
            data = self.session.get(url).json()
            total = data["hits"]["value"]
            current += 20
            yield from data["results"]

    def search(self, query, sort_by="size"):
        all_pages = []
        for content in self.generate_results(query):
            all_pages.append(content)

        # results = sorted(all_pages, key=lambda d: int(d["size"]), reverse=True)
        torrents = []

        for result in all_pages:
            torrents.append(
                {
                    "Name": result["title"],
                    "Size": get_hr_size(result["size"]),
                    "SE": result["swarm"]["leechers"],
                    "LE": result["swarm"]["leechers"],
                    "Site": "Solid Torrents",
                    "Magnet": result["magnet"],
                }
            )

        return torrents
