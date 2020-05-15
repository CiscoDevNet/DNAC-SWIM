#!/usr/bin/env python
from __future__ import print_function
import sys
import json
import logging
from argparse import ArgumentParser, REMAINDER

from util import get_url, post_and_wait, find_ids

def imageName2id(imageName):
    # if no image then return, will just use golden
    if imageName == None:
        return ""

    url='image/importation?name={0}'.format(imageName)
    response = get_url(url)
    return response['response'][0]['imageUuid']

def activate(imageUuid, *deviceIdList):

    body = []
    for deviceId in deviceIdList:
        body.append({
        "activateLowerImageVersion": True,
        "deviceUpgradeMode": "currentlyExists",
        "deviceUuid": deviceId,
        "distributeIfNeeded": False,
        "imageUuidList": [
            imageUuid
        ],
        "smuImageUuidList": [

        ]
    })

    url = 'image/activation/device'
    print(body)
    response = post_and_wait(url, body)

    print(response)
    taskId = response['id']
    detail = get_url('task?parentId={0}'.format(taskId))
    print (json.dumps(detail, indent=2))

def validate(imageUuid, *deviceIdList):
    '''
    quick check to make sure the image should be distributed to the device
    :param imageUuid:
    :param deviceIdList:
    :return:
    '''
    if imageUuid == "":
        print("using golden image, no validation")
        return
    image = get_url('image/importation/{0}'.format(imageUuid))
    print(image['response']['family'])
    for deviceId in deviceIdList:
        device = get_url('network-device/{0}'.format(deviceId))
        print(device['response']['series'])

if __name__ ==  "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--tag', type=str, required=False,
                        help="devices that match this tag")
    parser.add_argument('--image', type=str, required=False,
                        help="devices that match this tag")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    parser.add_argument('rest', nargs=REMAINDER, help="list of managemnet IP addresses")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    deviceIds = find_ids(args.tag, args.rest)
    if deviceIds == []:
        raise ValueError("No devices found for tag {}".format(args.tag))
    imageId = imageName2id(args.image)
    validate(imageId, *deviceIds)
    activate(imageId, *deviceIds)

