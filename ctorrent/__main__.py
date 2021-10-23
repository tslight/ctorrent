import curses
from argparse import ArgumentParser
from ctable import show_table
from .torrents import TPB, Solid, TorrentsCSV


def get_args():
    parser = ArgumentParser(description="search for torrents.")
    parser.add_argument("query", help="search query.")
    parser.add_argument(
        "-s", "--site",
        choices=["all", "csv", "tpb", "solid"],
        default="all",
        nargs="?",
        help="torrent website to search",
    )
    return parser.parse_args()


def main():
    args = get_args()
    if args.site == "all":
        tpb_torrents = TPB().search(args.query)
        solid_torrents = Solid().search(args.query)
        torrents = tpb_torrents + solid_torrents
    elif args.site == "tpb":
        torrents = TPB().search(args.query)
    elif args.site == "solid":
        torrents = Solid().search(args.query)
    elif args.site == "csv":
        torrents = TorrentsCSV().search(args.query)

    columns = ["Name", "Size", "SE", "LE", "Site"]
    show_table(torrents, columns)


if __name__ == "__main__":
    main()
