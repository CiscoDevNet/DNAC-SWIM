#!/usr/bin/env python
from __future__ import print_function
import sys
import json
import logging
from argparse import ArgumentParser

from util import get_url, post_and_wait, find_ids, delete_and_wait


def delete_file(file, *deviceIds):

    # need to check both filesystems for stack.
    for deviceId in deviceIds:
        url='device-image/device/{0}/file/{1}'.format(deviceId, file)
        response = delete_and_wait(url)
        print(response)


if __name__ ==  "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--tag', type=str, required=False,
                        help="devices that match this tag")
    parser.add_argument('--ips', type=str, required=False,
                        help="list of ip comma separated")
    parser.add_argument('--image', type=str, required=False,
                        help="devices that match this tag")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()

    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    deviceIds = find_ids(args.tag, args.ips)
    delete_file(args.image, *deviceIds)