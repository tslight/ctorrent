import curses
from argparse import ArgumentParser
from ctable import show_table
from .torrents import TPB


def get_args():
    parser = ArgumentParser(description="search for torrents.")
    parser.add_argument("query", help="search query.")
    return parser.parse_args()


def main():
    args = get_args()
    torrents = TPB().search(args.query)
    columns = ["name", "size", "seeders", "leechers"]
    print(show_table(torrents, columns))


if __name__ == "__main__":
    main()
