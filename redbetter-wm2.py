#!/usr/bin/env python2

from __future__ import unicode_literals

import requests
import argparse
import os
import configparser
import sys
from redapi import RedApi
from os import path
from sys import exit
from time import sleep

# cannonball approach but it werks (tm)
reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog='whatbetter')
    parser.add_argument('-s', '--snatches', type=int, help='minimum amount of snatches required before transcoding',
                        default=5)
    parser.add_argument('-b', '--better', type=int, help='better transcode search type', default=3)
    parser.add_argument('-c', '--count', type=int, help='maximum amount to queue (-1 for infinite)', default=5)
    parser.add_argument('-y', '--year', type=int, help='minimum release year', default=2016)
    parser.add_argument('-w', '--wait', type=int, help='wait X seconds between snatches', default=3)
    parser.add_argument('--320', action='store_true', help='Require 320 to be missing', default=False)
    parser.add_argument('--V0', action='store_true', help='Require V0 to be missing', default=False)
    parser.add_argument('--config', help='the location of the configuration file',
                        default=path.expanduser('~/.config/redbetter'))

    args = parser.parse_args()

    config = configparser.ConfigParser()
    try:
        open(args.config)
        config.read(args.config)
    except:
        if not path.exists(path.dirname(args.config)):
            os.makedirs(path.dirname(args.config))
        config.add_section('redacted')
        config.set('redacted', 'username', '')
        config.set('redacted', 'password', '')
        config.add_section('whatmanager')
        config.set('whatmanager', 'username', '')
        config.set('whatmanager', 'password', '')
        config.set('whatmanager', 'url', 'https://seedbox.example.com/transcode/request')
        config.write(open(args.config, 'w'))

        print("Please fill in the config at {}".format(args.config))
        exit(2)

    print("Authenticating")
    api = RedApi(config.get('redacted', 'username'), config.get('redacted', 'password'))

    found_count = 0
    while args.count > found_count >= 0:
        print("Grabbing better list")
        torrents = api.get_better(args.better)
        for torrent in torrents:
            for x in ['320', 'V0']:

                assert isinstance(args, argparse.Namespace)
                if args.__dict__[x] and not torrent["missing{}".format(x)]:
                    continue

            if torrent['groupYear'] < args.year:
                continue

            torrent_info = api.request('torrent', id=torrent['torrentId'])
            if torrent_info['torrent']['snatched'] < args.snatches:
                continue

            found_count += 1
            count_text = ''
            if args.count >= 0:
                count_text = "{}/{} ".format(found_count, args.count)

            print("{count_text}Snatching [{torrent[id]}] {group[musicInfo][artists][0][name]} - "
                  "{group[name]} ({group[year]}) | "
                  "Se {torrent[seeders]} Le {torrent[leechers]} Sn {torrent[snatched]}"
                  .format(count_text=count_text, **torrent_info))

            request_transcode(
                config.get('whatmanager', 'url'), config.get('whatmanager', 'username'),
                config.get('whatmanager', 'password'), torrent['torrentId']
            )

            if found_count >= args.count:
                break

            sleep(args.wait)


def request_transcode(url, username, password, torrent_id):
    return requests.post(url, auth=(username, password), data=dict(what_id=torrent_id)).json()['message']


if __name__ == '__main__':
    main()
