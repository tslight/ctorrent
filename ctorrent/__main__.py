import curses
from argparse import ArgumentParser
from ctable import show_table
from .torrents import TPB, Solid


def get_args():
    parser = ArgumentParser(description="search for torrents.")
    parser.add_argument("query", help="search query.")
    return parser.parse_args()


def main():
    args = get_args()
    tpb_torrents = TPB().search(args.query)
    solid_torrents = Solid().search(args.query)
    torrents = tpb_torrents + solid_torrents
    columns = ["Name", "Size", "Seeders", "Leechers", "Site"]
    print(show_table(torrents, columns))


if __name__ == "__main__":
    main()
