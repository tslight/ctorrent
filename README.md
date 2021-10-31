# CURSES TORRENT BROWSER

``` text
usage: ctorrent [-h] [-s [{all,csv,tpb,solid}]] [-c {all,audio,video,apps,games,porn,other}] [-o {size,seeders,leechers}] query

search for torrents.

positional arguments:
  query                 search query.

optional arguments:
  -h, --help            show this help message and exit
  -s [{all,csv,tpb,solid}], --site [{all,csv,tpb,solid}]
                        torrent website to search
  -c {all,audio,video,apps,games,porn,other}, --category {all,audio,video,apps,games,porn,other}
                        category to search in
  -o {size,seeders,leechers}, --order {size,seeders,leechers}
                        order to sort results in
```

## Keybindings

``` text
j, n, down  : Move down a row.
k, p, up    : Move up a row.
f, d, pgdn  : Move down a page.
b, u, pgup  : Move up a page.
g, <, home  : Go to first row.
G, >, end   : Go to last row.
v, i, enter : View row data.
q, x, escape: Exit.
```
