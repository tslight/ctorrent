import curses
from argparse import ArgumentParser
from .ctable import Table
from .torrents import TPB


def get_args():
    parser = ArgumentParser(description="search for torrents.")
    parser.add_argument("query", help="search query.")
    return parser.parse_args()


def get_magnet_link(stdscr):
    args = get_args()
    torrents = TPB().search(args.query)
    column_order = ["Name", "Size", "Seeders", "Leechers"]
    torrent_name = Table(stdscr, torrents, column_order).init()
    return next(
        (item for item in torrents if item["Name"] == torrent_name),
        None
    )["Magnet"]


def main():
    name = curses.wrapper(get_magnet_link)
    print(name)


if __name__ == "__main__":
    main()
