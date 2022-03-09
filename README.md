# ČTStream

Get MPEG-DASH streams from České televize

## CLI

### Help output

```txt
usage: ctstream.py [-h] [-t] [-n] [-r] channel

Get MPEG-DASH stream URLs from ČT

positional arguments:
  channel          Channel ID

options:
  -h, --help       show this help message and exit
  -t, --timeshift  Get timeshift stream
  -n, --newline    Print newline after stream URL
  -r, --traceback  Print traceback on error
```

### Examples

```sh
python ctstream.py 1
```

```sh
python ctstream.py 1 -t
```

## Channel IDs

```txt
1: ČT1
2: ČT2
3: ČT24
4: ČT sport
6: ČT :D / art
```

## Python API

### Get stream URL

```py
from ctstream import get_stream_url

ctstream.get_stream_url("1")
ctstream.get_stream_url("1", "main")
ctstream.get_stream_url("1", "timeshift")
```

### Get playlist url

```py
from ctstream import get_playlist_url

ctstream.get_playlist_url("1")
```

## Request flow

1. Get client playlist URL
   - `https://www.ceskatelevize.cz/ivysilani/ajax/get-client-playlist/`
2. Get stream URL from playlist
   - `https://www.ceskatelevize.cz/ivysilani/client-playlist/?key=<key>`

## Get channel IDs

Send GraphQL query to `https://api.ceskatelevize.cz/graphql/`:

```txt
query LiveBroadcastFind {
    liveBroadcastFind {
        id
        current {
            assignedToChannel {
                channelName
            }
        }
    }
}
```

## License

See [LICENSE](LICENSE) for license information.
