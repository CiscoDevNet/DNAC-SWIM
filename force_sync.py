#!/usr/bin/env python
from __future__ import print_function
import sys
import json
import logging
from argparse import ArgumentParser

from util import get_url, post_and_wait, find_ids, put_and_wait


def force_sync(deviceIds):

    payload= deviceIds
    url='network-device/sync?forceSync=true'

    response = put_and_wait(url, payload)
    print(response)


if __name__ ==  "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--tag', type=str, required=False,
                        help="devices that match this tag")
    parser.add_argument('--ips', type=str, required=False,
                        help="list of ip comma separated")
    args = parser.parse_args()

    deviceIds = find_ids(args.tag, args.ips)
    force_sync(deviceIds)