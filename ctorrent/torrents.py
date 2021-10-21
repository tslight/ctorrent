import requests
from urllib.parse import quote
from .utils import get_hr_size


class TPB:
    def __init__(self):
        self.base_url = "https://apibay.org"

    def get_magnet(self, info_hash, torrent_name):
        trackers = (
            "&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3"
            + "A%2F%2F9.rarbg.me%3A2850%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A29"
            + "20%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%"
            + "3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce"
        )
        return f"magnet:?xt=urn:btih:{info_hash}&dn={quote(torrent_name)}{trackers}"

    def search(self, query):
        url = f"{self.base_url}/q.php?q={query}"
        results = requests.get(url).json()
        results = sorted(results, key=lambda d: int(d["size"]), reverse=True)
        torrents = []

        for result in results:
            torrents.append(
                {
                    "Name": result["name"],
                    "Size": get_hr_size(result["size"]),
                    "Seeders": result["leechers"],
                    "Leechers": result["leechers"],
                    "Site": "The Pirate Bay",
                    "Magnet": self.get_magnet(result["info_hash"], result["name"]),
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
                    "Seeders": result["swarm"]["leechers"],
                    "Leechers": result["swarm"]["leechers"],
                    "Site": "Solid Torrents",
                    "Magnet": result["magnet"],
                }
            )

        return torrents
