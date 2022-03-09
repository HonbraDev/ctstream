"""
ČTStream
Author: HonbraDev (honbra.com)
Repository: https://github.com/honbradev/ctstream
License: MIT
"""

import sys
import requests
import json
import argparse


def get_playlist_url(channelId: str):
    url = "https://www.ceskatelevize.cz/ivysilani/ajax/get-client-playlist/"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-addr": "127.0.0.1"
    }

    data = {
        "playlist[0][type]": "channel",
        "playlist[0][id]": channelId,
        "requestUrl": "/ivysilani/embed/iFramePlayer.php",
        "requestSource": "iVysilani",
        "type": "html",
        "canPlayDRM": "false"
    }

    try:
        resp = requests.post(url, headers=headers, data=data)
    except:
        raise Exception("Error: Cannot connect to API")

    if resp.status_code != 200:
        raise Exception("Error: API returned status code " + str(resp.status_code))

    try:
        jesp = json.loads(resp.text)
    except:
        raise Exception("Error: Cannot parse JSON")

    if not "url" in jesp:
        raise Exception("Error: No stream url in response")

    if jesp["url"] == "Error":
        raise Exception("Error: Server-side error getting playlist url")

    return jesp["url"]


def get_stream_url(channelId: str, streamType="main"):
    playlist_url = get_playlist_url(channelId)

    try:
        resp = requests.get(playlist_url)
    except:
        raise Exception("Error: Cannot connect to playlist URL")

    try:
        jesp = json.loads(resp.text)
    except:
        raise Exception("Error: Cannot parse playlist JSON")

    if not "playlist" in jesp:
        raise Exception("Error: No playlist in response")

    if not isinstance(jesp["playlist"], list):
        raise Exception("Error: Playlist is not an array")

    if not "streamUrls" in jesp["playlist"][0]:
        raise Exception("Error: No stream URLs in playlist")

    if not streamType in jesp["playlist"][0]["streamUrls"]:
        raise Exception("Error: URL not found in playlist")

    return jesp["playlist"][0]["streamUrls"][streamType]


def main():
    parser = argparse.ArgumentParser(
        description="Get MPEG-DASH stream URLs from ČT")

    parser.add_argument(help="Channel ID", type=str, dest="channel")
    parser.add_argument("-t", "--timeshift",
                        help="Get timeshift stream", action="store_true")
    parser.add_argument(
        "-n", "--newline", help="Print newline after stream URL", action="store_true")
    parser.add_argument(
        "-r", "--traceback", help="Print traceback on error", action="store_true")

    args = parser.parse_args()

    try:
        stream_url = get_stream_url(
            args.channel, ("timeshift" if args.timeshift else "main"))
        sys.stdout.write(stream_url + ("\n" if args.newline else ""))
    except Exception as e:
        if args.traceback:
            raise
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
