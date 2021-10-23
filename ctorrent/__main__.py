import curses
from argparse import ArgumentParser
from ctable import show_table
from .torrents import TPB, Solid, CSV


def get_args():
    parser = ArgumentParser(description="search for torrents.")
    parser.add_argument("query", help="search query.")
    parser.add_argument(
        "-s",
        "--site",
        choices=["all", "csv", "tpb", "solid"],
        default="all",
        nargs="?",
        help="torrent website to search",
    )
    parser.add_argument(
        "-c",
        "--category",
        choices=[
            "all",
            "audio",
            "video",
            "apps",
            "games",
            "porn",
            "other",
        ],
        default="all",
        help="category to search in",
    )
    parser.add_argument(
        "-o",
        "--order",
        choices=[
            "size",
            "seeders",
            "leechers",
        ],
        default="seeders",
        help="order to sort results in",
    )

    return parser.parse_args()


def main():
    args = get_args()
    kwargs = {
        "query": args.query,
        "category": args.category,
        "order": args.order,
    }
    if args.site == "all":
        csv_torrents = CSV().search(**kwargs)
        tpb_torrents = TPB().search(**kwargs)
        solid_torrents = Solid().search(**kwargs)
        torrents = csv_torrents + solid_torrents + tpb_torrents
        torrents = sorted(torrents, key=lambda d: int(d[args.order]), reverse=True)
    elif args.site == "csv":
        torrents = CSV().search(**kwargs)
    elif args.site == "solid":
        torrents = Solid().search(**kwargs)
    elif args.site == "tpb":
        torrents = TPB().search(**kwargs)
    columns = ["Name", "Size", "SE", "LE", "Category", "Site"]
    show_table(torrents, columns)


if __name__ == "__main__":
    main()
